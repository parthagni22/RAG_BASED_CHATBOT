#!/usr/bin/env python3
"""
Setup script for Gemini + Pinecone RAG system
"""

import os
import json

def check_api_keys():
    """Check if API keys are configured"""
    print("🔑 Checking API keys...")
    
    try:
        from src.utils import load_keys
        keys = load_keys()
        
        gemini_key = keys.get("gemini", "")
        pinecone_key = keys.get("pinecone", "")
        openai_key = keys.get("openai", "")
        
        issues = []
        
        if not gemini_key or gemini_key == "<Enter your Gemini API key here>":
            issues.append("❌ Gemini API key not set")
            print("💡 Get free Gemini key at: https://aistudio.google.com/app/apikey")
        else:
            print("✅ Gemini API key found")
            
        if not pinecone_key or pinecone_key == "<Enter your own Pinecone key here>":
            issues.append("❌ Pinecone API key not set")
            print("💡 Get free Pinecone key at: https://www.pinecone.io/")
        else:
            print("✅ Pinecone API key found")
            
        if not openai_key or openai_key == "<Enter your own OpenAI key here>":
            print("⚠️  OpenAI key not set - will use free HuggingFace embeddings")
        else:
            print("✅ OpenAI key found - will use OpenAI embeddings")
            
        return len(issues) == 0, issues
        
    except Exception as e:
        return False, [f"❌ Error reading keys: {e}"]

def check_packages():
    """Check if required packages are installed"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        ("google.generativeai", "google-generativeai"),
        ("sentence_transformers", "sentence-transformers"),
        ("pinecone", "pinecone-client"),
        ("langchain_pinecone", "langchain-pinecone")
    ]
    
    missing_packages = []
    
    for import_name, install_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {install_name}")
        except ImportError:
            print(f"❌ {install_name}")
            missing_packages.append(install_name)
    
    return missing_packages

def check_pinecone_index():
    """Check if Pinecone index exists"""
    print("\n🌲 Checking Pinecone index...")
    
    try:
        from src.utils import load_keys
        from pinecone import Pinecone
        
        keys = load_keys()
        pinecone_key = keys.get("pinecone", "")
        
        if not pinecone_key or pinecone_key == "<Enter your own Pinecone key here>":
            print("❌ Pinecone API key not configured")
            return False
            
        pc = Pinecone(api_key=pinecone_key)
        indexes = pc.list_indexes()
        index_names = [idx.name for idx in indexes]
        
        if "indianconsti" in index_names:
            print("✅ Pinecone index 'indianconsti' found")
            
            # Check index dimensions
            index = pc.Index("indianconsti")
            stats = index.describe_index_stats()
            print(f"📊 Index stats: {stats}")
            return True
        else:
            print("❌ Pinecone index 'indianconsti' not found")
            print_index_instructions()
            return False
            
    except Exception as e:
        print(f"❌ Error checking Pinecone: {e}")
        return False

def print_index_instructions():
    """Print Pinecone index creation instructions"""
    print("\n" + "="*60)
    print("📝 PINECONE INDEX CREATION INSTRUCTIONS")
    print("="*60)
    print("1. Go to https://app.pinecone.io/")
    print("2. Sign in to your account")
    print("3. Click 'Create Index'")
    print("4. Use these settings:")
    print("   • Index Name: indianconsti")
    print("   • Dimensions: 1536 (if using OpenAI embeddings)")
    print("                 384 (if using free HuggingFace embeddings)")
    print("   • Metric: cosine")
    print("   • Cloud: AWS")
    print("   • Region: us-east-1")
    print("5. Click 'Create Index'")
    print("="*60)

def check_database():
    """Check if Database folder and files exist"""
    print("\n📁 Checking Database folder...")
    
    if not os.path.exists("Database/"):
        print("❌ Database/ folder not found")
        print("💡 Run: python create_simple_data.py")
        return False
    
    files = [f for f in os.listdir("Database/") if f.endswith(('.txt', '.pdf'))]
    if not files:
        print("❌ No .txt or .pdf files in Database/")
        print("💡 Run: python create_simple_data.py")
        return False
    
    print(f"✅ Found {len(files)} files in Database/:")
    for f in files[:5]:  # Show first 5 files
        print(f"   • {f}")
    if len(files) > 5:
        print(f"   ... and {len(files) - 5} more files")
    
    return True

def interactive_key_setup():
    """Interactive setup for API keys"""
    print("\n🔧 Interactive API Key Setup")
    print("-" * 30)
    
    # Get Gemini key
    print("\n1. Gemini API Key (FREE):")
    print("   Get it from: https://aistudio.google.com/app/apikey")
    gemini_key = input("   Enter your Gemini API key: ").strip()
    
    # Get Pinecone key  
    print("\n2. Pinecone API Key (FREE):")
    print("   Get it from: https://www.pinecone.io/")
    pinecone_key = input("   Enter your Pinecone API key: ").strip()
    
    # Optional OpenAI key
    print("\n3. OpenAI API Key (OPTIONAL - for better embeddings):")
    print("   Get it from: https://platform.openai.com/api-keys")
    print("   Leave blank to use free HuggingFace embeddings")
    openai_key = input("   Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if not openai_key:
        openai_key = ""
    
    # Save keys
    keys_data = {
        "gemini": gemini_key,
        "pinecone": pinecone_key,
        "openai": openai_key
    }
    
    try:
        os.makedirs("Data", exist_ok=True)
        with open("Data/keys.txt", "w") as f:
            json.dump(keys_data, f, indent=2)
        print("✅ API keys saved successfully!")
        return True
    except Exception as e:
        print(f"❌ Error saving keys: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Gemini + Pinecone RAG Setup")
    print("=" * 40)
    
    # Check packages
    missing_packages = check_packages()
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return
    
    # Check API keys
    keys_ok, issues = check_api_keys()
    if not keys_ok:
        print("\n".join(issues))
        response = input("\n❓ Set up API keys now? (y/n): ").lower()
        if response == 'y':
            if not interactive_key_setup():
                return
        else:
            print("📝 Please update Data/keys.txt with your API keys")
            return
    
    # Check database
    db_ok = check_database()
    
    # Check Pinecone index
    index_ok = check_pinecone_index()
    
    # Final summary
    print("\n" + "="*60)
    print("📊 SETUP SUMMARY")
    print("="*60)
    
    if keys_ok and db_ok and index_ok:
        print("🎉 Setup complete! You can now run:")
        print("   python AggieCourses.py  # Generate embeddings (one-time)")
        print("   python app.py           # Start the chatbot")
    else:
        print("⚠️  Setup incomplete. Please address:")
        if not db_ok:
            print("   • Run: python create_simple_data.py")
        if not index_ok:
            print("   • Create Pinecone index 'indianconsti'")

if __name__ == "__main__":
    main()