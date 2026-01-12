"""
Gemini API Manager for the Excel AI Assistant.
Handles interactions with Google's Gemini API.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple

import google.generativeai as genai


class GeminiAPIManager:
    """Manager for interacting with Google's Gemini API"""

    # Available Gemini models
    AVAILABLE_MODELS = [
        {"id": "models/gemini-2.0-flash", "name": "Gemini 2.0 Flash", "api": "gemini"},
        {"id": "models/gemini-2.0-flash-lite", "name": "Gemini 2.0 Flash Lite", "api": "gemini"},
        {"id": "models/gemini-2.5-flash", "name": "Gemini 2.5 Flash", "api": "gemini"},
        {"id": "models/gemini-2.5-pro", "name": "Gemini 2.5 Pro", "api": "gemini"},
    ]

    def __init__(self, api_key: str = "", model: str = "gemini-1.5-flash"):
        """Initialize the Gemini API manager"""
        self.api_key = api_key
        self.model = model
        self.client = None
        self.logger = logging.getLogger("GeminiAPIManager")

        if api_key:
            self.initialize(api_key)

    def initialize(self, api_key: Optional[str] = None) -> bool:
        """Initialize the Gemini API client"""
        if api_key:
            self.api_key = api_key

        if not self.api_key:
            self.logger.error("API Key is required for Gemini")
            return False

        try:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini client: {e}")
            return False

    def set_model(self, model: str) -> None:
        """Set the model to use for API calls"""
        self.model = model
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model)
            except Exception as e:
                self.logger.error(f"Failed to set model: {e}")

    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available Gemini models"""
        return self.AVAILABLE_MODELS.copy()

    def test_connection(self) -> Tuple[bool, str]:
        """Test the Gemini API connection"""
        if not self.client:
            if not self.initialize():
                return False, "Gemini API client not initialized"

        try:
            response = self.client.generate_content(
                "Test connection - respond with just 'OK'",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=10,
                    temperature=0.1
                )
            )

            if response and response.text:
                return True, "Gemini connection successful"
            else:
                return False, "Invalid response from Gemini API"

        except Exception as e:
            return False, f"Gemini Error: {str(e)}"

    def process_single_cell(
            self,
            cell_content: str,
            system_prompt: str,
            user_prompt: str,
            temperature: float = 0.3,
            max_tokens: int = 150,
            context_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Process a single cell using Gemini API

        Args:
            cell_content: The content of the cell being processed
            system_prompt: System prompt for the AI
            user_prompt: User prompt for the AI
            temperature: Temperature parameter for generation
            max_tokens: Maximum tokens in response
            context_data: Optional dictionary with context data from other columns

        Returns:
            Tuple of (success, result, error_message)
        """
        if not self.client:
            if not self.initialize():
                return False, None, "Gemini API client not initialized"

        # Build the full prompt
        formatted_prompt = f"{system_prompt}\n\n{user_prompt}\n\nCell content: {cell_content}"

        # Add context information if available
        if context_data and len(context_data) > 0:
            context_text = "\n\nContext information:\n"
            for key, value in context_data.items():
                context_text += f"- {key}: {value}\n"
            formatted_prompt += context_text

        try:
            response = self.client.generate_content(
                formatted_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )

            if response and response.text:
                result = response.text.strip()
                return True, result, None
            else:
                return False, None, "Empty response from Gemini API"

        except Exception as e:
            self.logger.error(f"Gemini API Error: {str(e)}")
            return False, None, f"Gemini Error: {str(e)}"
