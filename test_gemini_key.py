#!/usr/bin/env python3
"""
Test Gemini API key
"""

import google.generativeai as genai
from src.utils import load_keys

# Load keys
keys = load_keys()
gemini_key = keys.get("gemini", "")

print(f"Testing Gemini API key: {gemini_key[:20]}...")

try:
    # Configure Gemini
    genai.configure(api_key=gemini_key)
    
    # Test the API
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Hello, API is working!'")
    
    print("✅ Gemini API key is valid!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ Gemini API key is invalid!")
    print(f"Error: {e}")
    print("\n🔧 Please:")
    print("1. Get a new API key from: https://aistudio.google.com/app/apikey")
    print("2. Update Data/keys.txt with the correct key")
    print("3. Make sure there are no extra spaces or characters")