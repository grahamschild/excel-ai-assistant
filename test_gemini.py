"""
Quick test to check which Gemini models are available with your API key.
Run this from the excel-ai-assistant directory.
"""
import google.generativeai as genai

# Replace with your actual API key
API_KEY = "import google.generativeai as genai

# Replace with your actual API key
API_KEY = "AIzaSyCum_bPtFDFgbcK80G7PPtK2maoo5_8hhA"

genai.configure(api_key=API_KEY)

print("Listing available models...")
for model in genai.list_models():
    if "gemini" in model.name.lower():
        print(f"  - {model.name}")
"

genai.configure(api_key=API_KEY)

print("Listing available models...")
for model in genai.list_models():
    if "gemini" in model.name.lower():
        print(f"  - {model.name}")
