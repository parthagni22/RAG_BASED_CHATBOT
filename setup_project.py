#!/usr/bin/env python3
"""
Setup script for the RAG Chatbot project
This script helps you set up the project step by step
"""

import os
import json
from src.utils import load_keys

def check_api_keys():
    """Check if API keys are properly configured"""
    print("🔑 Checking API keys...")
    
    try:
        keys = load_keys()
        
        openai_key = keys.get("openai", "")
        pinecone_key = keys.get("pinecone", "")
        
        if openai_key == "<Enter your own OpenAI key here>" or not openai_key:
            print("❌ OpenAI API key not set")
            return False
        else:
            print("✅ OpenAI API key found")
            
        if pinecone_key == "<Enter your own Pinecone key here>" or not pinecone_key:
            print("❌ Pinecone API key not set")
            return False
        else:
            print("✅ Pinecone API key found")
            
        return True
        
    except Exception as e:
        print(f"❌ Error reading keys: {e}")
        return False

def check_database_folder():
    """Check if Database folder exists and has PDF files"""
    print("\n📁 Checking Database folder...")
    
    if not os.path.exists("Database/"):
        print("❌ Database/ folder not found")
        print("💡 Creating Database/ folder...")
        os.makedirs("Database/")
        print("✅ Database/ folder created")
        print("📝 Please add your PDF files to the Database/ folder")
        return False
    
    pdf_files = [f for f in os.listdir("Database/") if f.endswith('.pdf')]
    if not pdf_files:
        print("❌ No PDF files found in Database/ folder")
        print("📝 Please add your PDF files to the Database/ folder")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF files in Database/ folder")
    return True

def check_pinecone_index():
    """Check if Pinecone index exists"""
    print("\n🌲 Checking Pinecone index...")
    
    try:
        from pinecone import Pinecone
        keys = load_keys()
        
        if keys["pinecone"] == "<Enter your own Pinecone key here>":
            print("❌ Pinecone API key not configured")
            return False
            
        pc = Pinecone(api_key=keys["pinecone"])
        indexes = pc.list_indexes()
        index_names = [idx.name for idx in indexes]
        
        if "indianconsti" in index_names:
            print("✅ Pinecone index 'indianconsti' found")
            return True
        else:
            print("❌ Pinecone index 'indianconsti' not found")
            print_index_creation_instructions()
            return False
            
    except Exception as e:
        print(f"❌ Error checking Pinecone: {e}")
        return False

def print_index_creation_instructions():
    """Print instructions for creating Pinecone index"""
    print("\n" + "="*60)
    print("📝 PINECONE INDEX CREATION INSTRUCTIONS")
    print("="*60)
    print("1. Go to https://app.pinecone.io/")
    print("2. Sign in to your account")
    print("3. Click 'Create Index'")
    print("4. Use these settings:")
    print("   • Index Name: indianconsti")
    print("   • Dimensions: 1536")
    print("   • Metric: cosine")
    print("   • Cloud: AWS")
    print("   • Region: us-east-1")
    print("5. Click 'Create Index'")
    print("="*60)

def setup_keys_interactive():
    """Interactive setup for API keys"""
    print("\n🔧 Interactive API Key Setup")
    print("-" * 30)
    
    openai_key = input("Enter your OpenAI API key: ").strip()
    pinecone_key = input("Enter your Pinecone API key: ").strip()
    
    keys_data = {
        "openai": openai_key,
        "pinecone": pinecone_key
    }
    
    try:
        with open("Data/keys.txt", "w") as f:
            json.dump(keys_data, f, indent=2)
        print("✅ API keys saved successfully!")
        return True
    except Exception as e:
        print(f"❌ Error saving keys: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 RAG Chatbot Project Setup")
    print("=" * 40)
    
    # Check if Data folder exists
    if not os.path.exists("Data/"):
        print("Creating Data/ folder...")
        os.makedirs("Data/")
    
    # Check API keys
    if not check_api_keys():
        response = input("\n❓ Would you like to set up API keys now? (y/n): ").lower()
        if response == 'y':
            if not setup_keys_interactive():
                print("❌ Setup failed. Please manually edit Data/keys.txt")
                return
        else:
            print("📝 Please manually edit Data/keys.txt with your API keys")
            return
    
    # Check database folder
    database_ready = check_database_folder()
    
    # Check Pinecone index
    index_ready = check_pinecone_index()
    
    # Final status
    print("\n" + "="*60)
    print("📊 SETUP SUMMARY")
    print("="*60)
    
    if check_api_keys() and database_ready and index_ready:
        print("🎉 Setup complete! You can now run:")
        print("   python generate_embeddings.py  # (one-time)")
        print("   python app.py                  # (to start the app)")
    else:
        print("⚠️  Setup incomplete. Please address the issues above.")
        if not database_ready:
            print("   • Add PDF files to Database/ folder")
        if not index_ready:
            print("   • Create Pinecone index 'indianconsti'")

if __name__ == "__main__":
    main()