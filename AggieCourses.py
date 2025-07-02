import os
from src.utils import load_keys
import time 
from pinecone import Pinecone  # Updated import
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.schema import (
    SystemMessage,
    HumanMessage
)
from dotenv import load_dotenv
load_dotenv()

# Load keys properly
keys = load_keys()
os.environ["OPENAI_API_KEY"] = keys.get("openai", "")
os.environ["PINECONE_API_KEY"] = keys.get("pinecone", "")
gemini_api_key = keys.get("gemini", "")

class AggieeRag:
    def __init__(self) -> None:
        # Check if API keys are properly set
        if not gemini_api_key or gemini_api_key == "<Enter your Gemini API key here>":
            raise ValueError("Please set your Gemini API key in Data/keys.txt")
        if os.environ["PINECONE_API_KEY"] == "<Enter your own Pinecone key here>":
            raise ValueError("Please set your Pinecone API key in Data/keys.txt")
        
        # Configure and initialize Gemini
        genai.configure(api_key=gemini_api_key)
        self.chatbot = genai.GenerativeModel('gemini-1.5-flash')
        
        # For embeddings, use free HuggingFace since OpenAI key is empty
        try:
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.use_sentence_transformers = True
            print("✅ Using free HuggingFace embeddings (384 dimensions)")
        except ImportError:
            raise ImportError("Please install sentence-transformers: pip install sentence-transformers")
        
        # Initialize Pinecone (UPDATED METHOD)
        self.pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        self.index_name = "indianconsti"
        self.index = self.init_pinecone()
        
        # System message for Gemini
        self.system_prompt = """You are a University Course Information Assistant for Texas A&M University's CSCE (Computer Science & Engineering) and ECEN (Electrical & Computer Engineering) departments. 

Your responsibilities:
- Provide accurate, reliable information about graduate-level courses and programs
- Base responses exclusively on the provided context from official PDFs and documents
- Include specific details like course numbers, credit hours, prerequisites, and requirements
- Help students understand degree plans, specializations, and academic policies

Guidelines for responses:
- Give detailed, helpful answers when context supports it
- Include relevant course codes, credit hours, and prerequisites
- Explain degree requirements clearly and completely
- Reference specific policies and guidelines when mentioned in documents
- If information is insufficient, clearly state what you don't know
- Always be factual and avoid speculation beyond the provided documents

Focus areas:
- Course descriptions and requirements
- MS and PhD degree plan requirements  
- Specializations and research areas
- Academic rules, guidelines, and policies
- Prerequisites and course sequencing"""

        self.messages = [
            SystemMessage(content=self.system_prompt)
        ]

    def init_pinecone(self):
        """Connect to Pinecone index"""
        try:
            # Get the index using the new Pinecone client
            self.index = self.pc.Index(self.index_name)
            time.sleep(1)
            print(f"✅ Connected to Pinecone index: {self.index_name}")
            return self.index
        except Exception as e:
            print(f"❌ Error connecting to Pinecone index '{self.index_name}': {e}")
            raise
    
    def generate_insert_embeddings_(self, docs):
        """Generate and insert embeddings into Pinecone"""
        print(f"🔄 Generating embeddings for {len(docs)} document chunks...")
        batch_size = 50  # Smaller batches for free tier
        
        for i in range(0, len(docs), batch_size):
            batch = docs[i:i + batch_size]
            vectors_to_upsert = []
            
            try:
                # Prepare texts for embedding
                texts = [doc.page_content for doc in batch]
                
                # Generate embeddings using sentence transformers
                embeddings_list = self.embedding_model.encode(texts).tolist()
                
                # Create vectors for Pinecone
                for j, (doc, embedding) in enumerate(zip(batch, embeddings_list)):
                    doc_id = str(i + j)
                    
                    vector_data = {
                        "id": doc_id,
                        "values": embedding,
                        "metadata": {
                            "text": doc.page_content[:1000],  # Limit text length for metadata
                            "source": getattr(doc, 'metadata', {}).get('source', 'unknown'),
                            "chunk_id": doc_id
                        }
                    }
                    vectors_to_upsert.append(vector_data)
                
                # Upsert batch to Pinecone
                self.index.upsert(vectors=vectors_to_upsert)
                print(f"📤 Uploaded batch {i//batch_size + 1}/{(len(docs) + batch_size - 1)//batch_size}")
                
                # Small delay to avoid rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error processing batch {i//batch_size + 1}: {e}")
                continue
            
        print("🎉 Embedding generation completed!")

    def chunk_data(self, docs, chunk_size=800, chunk_overlap=50):
        """Chunk documents into smaller pieces"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.doc = self.text_splitter.split_documents(docs)
        print(f"✂️ Created {len(self.doc)} chunks from {len(docs)} documents")
        return self.doc

    def read_doc(self, directory):
        """Read documents from directory"""
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory '{directory}' not found. Please create it and add your files.")
        
        # Load text files
        documents = []
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            # Create a document-like object
                            doc = type('Document', (), {
                                'page_content': content,
                                'metadata': {'source': filename}
                            })()
                            documents.append(doc)
                except Exception as e:
                    print(f"⚠️ Error reading {filename}: {e}")
        
        # Try to load PDFs
        try:
            file_loader = PyPDFDirectoryLoader(directory)
            pdf_documents = file_loader.load()
            documents.extend(pdf_documents)
            print(f"📄 Loaded {len(pdf_documents)} PDF files")
        except Exception as e:
            print(f"Note: Could not load PDFs: {e}")
        
        if not documents:
            raise ValueError(f"No readable documents found in '{directory}'. Please add some .txt or .pdf files.")
            
        print(f"📚 Loaded {len(documents)} documents from {directory}")
        return documents
    
    def search_similar_chunks(self, query, k=3):
        """Search for similar chunks in Pinecone"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])[0].tolist()
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=k,
                include_metadata=True
            )
            
            # Extract relevant chunks
            relevant_chunks = []
            for match in results['matches']:
                if match['score'] > 0.1:  # Lowered similarity threshold for HuggingFace embeddings
                    relevant_chunks.append({
                        'content': match['metadata'].get('text', ''),
                        'source': match['metadata'].get('source', 'unknown'),
                        'score': match['score']
                    })
            
            return relevant_chunks
            
        except Exception as e:
            print(f"❌ Error searching Pinecone: {e}")
            return []
    
    def augment_prompt(self, query: str):
        """Search Pinecone and generate response with Gemini"""
        try:
            # Search for relevant documents
            relevant_chunks = self.search_similar_chunks(query, k=3)
            
            if not relevant_chunks:
                return "I don't have specific information about that topic in my current database. Please try rephrasing your question or ask about Texas A&M CSCE/ECEN courses and degree requirements."
            
            # Extract text from results
            source_knowledge = "\n\n---\n\n".join([
                f"Source: {chunk['source']}\nContent: {chunk['content']}"
                for chunk in relevant_chunks
            ])
            
            # Create prompt for Gemini
            full_prompt = f"""{self.system_prompt}

CONTEXT INFORMATION:
{source_knowledge}

STUDENT QUESTION: {query}

Please provide a comprehensive and helpful response based on the context information above. Include specific details like course numbers, credit hours, prerequisites, and requirements when available."""

            # Generate response with Gemini
            response = self.chatbot.generate_content(full_prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
            
        except Exception as e:
            print(f"❌ Error in augment_prompt: {e}")
            return f"I encountered an error while processing your question: {str(e)}. Please try again."


# Compatibility wrapper for Gemini
class GeminiChatBot:
    def __init__(self, rag_system):
        self.rag_system = rag_system

    def __call__(self, messages):
        # Extract the last human message
        last_message = messages[-1].content if messages else ""
        response_text = self.rag_system.augment_prompt(last_message)
        
        # Return a response object compatible with existing code
        class Response:
            def __init__(self, content):
                self.content = content
        
        return Response(response_text)


# Example usage for generating embeddings
if __name__ == "__main__":
    try:
        print("🚀 Initializing Gemini + Pinecone RAG system...")
        llm = AggieeRag()
        
        # Check if Database folder exists
        if not os.path.exists("Database/"):
            print("❌ Database/ folder not found")
            print("💡 Please run: python create_simple_data.py")
            exit(1)
        
        # Generate embeddings
        print("📖 Reading documents...")
        docs = llm.read_doc("Database/")
        
        print("✂️ Chunking documents...")
        documents = llm.chunk_data(docs=docs)
        
        print("🚀 Generating and uploading embeddings to Pinecone...")
        llm.generate_insert_embeddings_(documents)
        
        print("\n🎉 SUCCESS! Embeddings generated and uploaded to Pinecone")
        print("✅ Your Gemini + Pinecone RAG system is ready!")
        
        # Test the system
        test_query = "Texas A&M CSCE/ECEN courses and degree requirements"
        print(f"\n🧪 Testing with query: {test_query}")
        response = llm.augment_prompt(test_query)
        print(f"🤖 Response: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Gemini and Pinecone API keys are set in Data/keys.txt")
        print("2. Ensure Pinecone index 'indianconsti' exists with 384 dimensions")
        print("3. Check that Database/ folder has documents")
        print("4. Install required packages: pip install sentence-transformers")