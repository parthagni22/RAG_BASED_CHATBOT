import os
import json
import time
import numpy as np
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import SystemMessage, HumanMessage

def load_keys():
    """Load API keys from keys.txt file"""
    try:
        with open("Data/keys.txt", 'r') as f:
            keys = json.load(f)
        return keys
    except FileNotFoundError:
        print("❌ Data/keys.txt not found")
        return {}

class GeminiAggieeRag:
    """
    RAG implementation using:
    - Google Gemini for text generation (FREE)
    - Sentence Transformers for embeddings (FREE)
    - Local vector storage instead of Pinecone (FREE)
    """

    def __init__(self) -> None:
        print("🚀 Initializing Gemini RAG system...")
        
        # Load API keys
        self.keys = load_keys()
        gemini_key = self.keys.get("gemini", "")
        
        if not gemini_key or gemini_key == "<Enter your Gemini API key here>":
            raise ValueError("Please set your Gemini API key in Data/keys.txt")
        
        # Configure Gemini
        genai.configure(api_key=gemini_key)
        
        # Initialize Gemini model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize embedding system
        print("📥 Loading embedding model...")
        try:
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.use_sentence_transformers = True
        except ImportError:
            print("⚠️ sentence-transformers not installed. Using TF-IDF as fallback...")
            self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            self.use_sentence_transformers = False
        
        # Storage for document embeddings
        self.document_chunks = []
        self.document_embeddings = []
        self.chunk_metadata = []
        
        # System message
        self.system_prompt = """You are a University Course Information Assistant for Texas A&M University's CSCE (Computer Science & Engineering) and ECEN (Electrical & Computer Engineering) departments. 

Your role:
- Provide accurate information about courses, degree requirements, and academic policies
- Base your answers on the provided context documents
- Be helpful and informative
- If you don't have enough information, say so clearly
- Always reference the source when possible

Guidelines:
- Give detailed responses when appropriate
- Include specific course numbers, credit hours, and prerequisites when available
- Explain degree requirements clearly
- Help students understand academic policies"""

    def load_documents(self, directory: str):
        """Load documents from directory"""
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory '{directory}' not found. Please create it and add your files.")
        
        documents = []
        
        # Load text files
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():  # Only add non-empty files
                            documents.append({
                                'content': content,
                                'source': filename
                            })
                except Exception as e:
                    print(f"⚠️ Error reading {filename}: {e}")
        
        # Try to load PDFs if available
        try:
            from langchain_community.document_loaders import PyPDFDirectoryLoader
            file_loader = PyPDFDirectoryLoader(directory)
            pdf_docs = file_loader.load()
            for doc in pdf_docs:
                if hasattr(doc, 'page_content') and doc.page_content.strip():
                    documents.append({
                        'content': doc.page_content,
                        'source': getattr(doc, 'metadata', {}).get('source', 'unknown.pdf')
                    })
        except Exception as e:
            print(f"Note: Could not load PDFs: {e}")
        
        if not documents:
            raise ValueError(f"No readable documents found in '{directory}'. Please add some .txt or .pdf files.")
        
        return documents

    def chunk_documents(self, documents: List[Dict], chunk_size=800, chunk_overlap=100):
        """Split documents into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        chunks = []
        for doc in documents:
            doc_chunks = text_splitter.split_text(doc['content'])
            for i, chunk in enumerate(doc_chunks):
                if chunk.strip():  # Only add non-empty chunks
                    chunks.append({
                        'content': chunk.strip(),
                        'source': doc['source'],
                        'chunk_id': f"{doc['source']}_chunk_{i}"
                    })
        
        return chunks

    def generate_embeddings(self, chunks: List[Dict]):
        """Generate embeddings for document chunks"""
        print(f"🔄 Generating embeddings for {len(chunks)} chunks...")
        
        self.document_chunks = chunks
        texts = [chunk['content'] for chunk in chunks]
        
        if self.use_sentence_transformers:
            # Use sentence transformers
            self.document_embeddings = self.embedding_model.encode(texts)
        else:
            # Fallback to TF-IDF
            self.document_embeddings = self.tfidf_vectorizer.fit_transform(texts)
        
        self.chunk_metadata = [{'source': chunk['source'], 'chunk_id': chunk['chunk_id']} for chunk in chunks]
        print("✅ Embeddings generated successfully!")

    def search_similar_chunks(self, query: str, k: int = 3):
        """Find most similar chunks to query"""
        if not self.document_chunks:
            return []
        
        if self.use_sentence_transformers:
            # Use sentence transformers
            query_embedding = self.embedding_model.encode([query])
            similarities = cosine_similarity(query_embedding, self.document_embeddings)[0]
        else:
            # Use TF-IDF
            query_tfidf = self.tfidf_vectorizer.transform([query])
            similarities = cosine_similarity(query_tfidf, self.document_embeddings)[0]
        
        # Get top k most similar chunks
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                results.append({
                    'content': self.document_chunks[idx]['content'],
                    'source': self.document_chunks[idx]['source'],
                    'chunk_id': self.document_chunks[idx]['chunk_id'],
                    'similarity': similarities[idx]
                })
        
        return results

    def generate_response_with_gemini(self, query: str, context_chunks: List[Dict]) -> str:
        """Generate response using Gemini"""
        
        # Prepare context
        context_parts = []
        for chunk in context_chunks:
            context_parts.append(f"Source: {chunk['source']}\nContent: {chunk['content']}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Create prompt for Gemini
        prompt = f"""{self.system_prompt}

CONTEXT INFORMATION:
{context}

STUDENT QUESTION: {query}

Please provide a helpful and accurate response based on the context information above. If the context doesn't contain enough information to fully answer the question, please say so and provide what information you can."""

        try:
            # Generate response with Gemini
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
                
        except Exception as e:
            print(f"Error generating response with Gemini: {e}")
            return f"I encountered an error while processing your question. Please try again. Error: {str(e)}"

    def augment_prompt(self, query: str) -> str:
        """Main method to process query and return response"""
        try:
            if not self.document_chunks:
                return "The system hasn't been initialized with documents yet. Please make sure documents are loaded."
            
            # Search for relevant chunks
            relevant_chunks = self.search_similar_chunks(query, k=3)
            
            if not relevant_chunks:
                return """I don't have specific information about that topic in my current database. 

For the most accurate and up-to-date information about Texas A&M University courses and programs, I recommend:
- Checking the official Texas A&M course catalog
- Contacting the CSCE or ECEN department directly
- Speaking with an academic advisor

Is there anything else about the available course information I can help you with?"""
            
            # Generate response using Gemini
            response = self.generate_response_with_gemini(query, relevant_chunks)
            
            return response
            
        except Exception as e:
            return f"I apologize, but I encountered an error processing your question: {str(e)}"

    def setup_from_directory(self, directory: str):
        """Complete setup from document directory"""
        print("📚 Loading documents...")
        documents = self.load_documents(directory)
        print(f"✅ Loaded {len(documents)} documents")
        
        print("✂️ Chunking documents...")
        chunks = self.chunk_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")
        
        print("🔄 Generating embeddings...")
        self.generate_embeddings(chunks)
        
        print("🎉 Setup complete! Ready to answer questions.")


# Compatibility wrapper for existing app.py
class GeminiChatBot:
    def __init__(self, rag_system):
        self.rag_system = rag_system

    def __call__(self, messages):
        # Extract the last human message
        last_message = messages[-1].content if messages else ""
        response_text = self.rag_system.augment_prompt(last_message)
        
        # Return a response object
        class Response:
            def __init__(self, content):
                self.content = content
        
        return Response(response_text)


# Main class for compatibility with existing app.py
class AggieeRag:
    def __init__(self):
        self.gemini_rag = GeminiAggieeRag()
        self.chatbot = GeminiChatBot(self.gemini_rag)
        self.messages = [
            SystemMessage(content=self.gemini_rag.system_prompt)
        ]
        self._setup_complete = False

    def setup_from_directory(self, directory: str):
        """Setup the system with documents"""
        self.gemini_rag.setup_from_directory(directory)
        self._setup_complete = True

    def augment_prompt(self, query: str) -> str:
        """Process query and return response"""
        if not self._setup_complete:
            # Try to auto-setup if Database exists
            if os.path.exists("Database"):
                try:
                    self.setup_from_directory("Database")
                except Exception as e:
                    return f"Error initializing system: {str(e)}"
            else:
                return "System not initialized. Please create a 'Database' folder and add your documents, then restart the application."
        
        return self.gemini_rag.augment_prompt(query)


if __name__ == "__main__":
    # Test the system
    try:
        print("🚀 Testing Gemini RAG System...")
        rag = AggieeRag()
        
        if os.path.exists("Database"):
            rag.setup_from_directory("Database")
            
            # Test queries
            test_queries = [
                "What are the requirements for MS in Computer Science?",
                "Tell me about CSCE 629",
                "What prerequisites does the Deep Learning course have?"
            ]
            
            for query in test_queries:
                print(f"\n📝 Query: {query}")
                response = rag.augment_prompt(query)
                print(f"🤖 Response: {response}")
                print("-" * 50)
        else:
            print("❌ Database folder not found. Run create_simple_data.py first")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have set up your Gemini API key in Data/keys.txt")