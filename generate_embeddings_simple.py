#!/usr/bin/env python3
"""
Simple script to generate embeddings for your documents
"""

from AggieCourses import AggieeRag
import os

def main():
    """Generate embeddings for documents in Database/ folder"""
    
    print("🚀 Starting embedding generation...")
    print("-" * 40)
    
    try:
        # Check if Database folder exists
        if not os.path.exists("Database/"):
            print("❌ Database/ folder not found")
            print("💡 Run 'python create_simple_data.py' first")
            return
        
        # Check if there are files
        files = [f for f in os.listdir("Database/") if f.endswith(('.txt', '.pdf'))]
        if not files:
            print("❌ No .txt or .pdf files found in Database/")
            print("💡 Run 'python create_simple_data.py' first")
            return
        
        print(f"📚 Found {len(files)} files:")
        for f in files:
            print(f"   • {f}")
        
        # Initialize RAG system
        print("\n🔄 Initializing RAG system...")
        llm = AggieeRag()
        
        # Read documents
        print("📖 Reading documents...")
        docs = llm.read_doc("Database/")
        print(f"✅ Loaded {len(docs)} document pages")
        
        # Chunk documents
        print("✂️  Chunking documents...")
        documents = llm.chunk_data(docs=docs)
        print(f"✅ Created {len(documents)} text chunks")
        
        # Generate embeddings
        print("🚀 Generating and uploading embeddings...")
        llm.generate_insert_embeddings_(documents)
        
        print("\n🎉 SUCCESS! Embeddings generated and uploaded to Pinecone")
        print("✅ Your chatbot is now ready to answer questions!")
        print("\n🎯 Next step: Run 'python app.py' to start the chatbot")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure your API keys are set in Data/keys.txt")
        print("2. Ensure Pinecone index 'indianconsti' exists")
        print("3. Check that Database/ folder has files")

if __name__ == "__main__":
    main()