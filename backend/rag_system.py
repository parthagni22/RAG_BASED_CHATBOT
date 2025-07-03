#!/usr/bin/env python3
"""
Improved RAG system with better error handling, caching, and flexibility
"""

import hashlib
import logging
import pickle
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import google.generativeai as genai
import numpy as np
from langchain.schema import SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import cosine_similarity

from config import config


@dataclass
class DocumentChunk:
    """Represents a document chunk with metadata"""

    content: str
    source: str
    chunk_id: str
    metadata: Dict = None


@dataclass
class SearchResult:
    """Represents a search result"""

    chunk: DocumentChunk
    similarity: float


class EmbeddingManager:
    """Manages different embedding providers"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.embedding_model = None
        self.provider = self._select_provider()
        self._initialize_embeddings()

    def _select_provider(self) -> str:
        """Select the best available embedding provider"""
        if config.openai_api_key:
            try:
                import openai

                return "openai"
            except ImportError:
                self.logger.warning(
                    "OpenAI API key provided but openai package not installed. Falling back to SentenceTransformers."
                )
                return "sentence_transformers"
        else:
            return "sentence_transformers"

    def _initialize_embeddings(self):
        """Initialize the embedding model"""
        try:
            if self.provider == "openai":
                try:
                    import openai

                    # For newer OpenAI versions (v1.0+)
                    self.openai_client = openai.OpenAI(api_key=config.openai_api_key)
                    self.embedding_dim = 1536
                    self.logger.info("Using OpenAI embeddings")
                except ImportError:
                    self.logger.warning(
                        "OpenAI package not available, falling back to SentenceTransformers"
                    )
                    self.provider = "sentence_transformers"
                    self._initialize_sentence_transformers()
                except Exception as e:
                    self.logger.error(
                        f"Failed to initialize OpenAI: {e}. Falling back to SentenceTransformers"
                    )
                    self.provider = "sentence_transformers"
                    self._initialize_sentence_transformers()
            else:
                self._initialize_sentence_transformers()
        except Exception as e:
            self.logger.error(f"Failed to initialize embeddings: {e}")
            raise

    def _initialize_sentence_transformers(self):
        """Initialize SentenceTransformers"""
        try:
            from sentence_transformers import SentenceTransformer

            self.embedding_model = SentenceTransformer(config.embedding_model)
            self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
            self.logger.info(
                f"Using SentenceTransformers embeddings ({self.embedding_dim}D)"
            )
        except ImportError:
            raise ImportError(
                "sentence-transformers package is required but not installed. Please install it with: pip install sentence-transformers"
            )

    def encode(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for texts"""
        try:
            if self.provider == "openai":
                try:
                    response = self.openai_client.embeddings.create(
                        input=texts, model="text-embedding-ada-002"
                    )
                    embeddings = [item.embedding for item in response.data]
                    return np.array(embeddings)
                except Exception as e:
                    self.logger.error(
                        f"OpenAI embedding failed: {e}. Falling back to SentenceTransformers"
                    )
                    # Fall back to SentenceTransformers
                    self.provider = "sentence_transformers"
                    if not self.embedding_model:
                        self._initialize_sentence_transformers()
                    return self.embedding_model.encode(texts)
            else:
                return self.embedding_model.encode(texts)
        except Exception as e:
            self.logger.error(f"Failed to generate embeddings: {e}")
            raise


class VectorStore:
    """Abstract base class for vector storage"""

    def add_documents(self, chunks: List[DocumentChunk], embeddings: np.ndarray):
        raise NotImplementedError

    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[SearchResult]:
        raise NotImplementedError


class LocalVectorStore(VectorStore):
    """Local vector storage using numpy and pickle"""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_file = cache_dir / "vector_store.pkl"
        self.chunks: List[DocumentChunk] = []
        self.embeddings: Optional[np.ndarray] = None
        self.logger = logging.getLogger(__name__)
        self._load_cache()

    def _load_cache(self):
        """Load cached vectors if available"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "rb") as f:
                    data = pickle.load(f)
                    self.chunks = data["chunks"]
                    self.embeddings = data["embeddings"]
                self.logger.info(f"Loaded {len(self.chunks)} cached vectors")
            except Exception as e:
                self.logger.warning(f"Failed to load cache: {e}")

    def _save_cache(self):
        """Save vectors to cache"""
        try:
            self.cache_dir.mkdir(exist_ok=True)
            with open(self.cache_file, "wb") as f:
                pickle.dump({"chunks": self.chunks, "embeddings": self.embeddings}, f)
            self.logger.info("Vector cache saved")
        except Exception as e:
            self.logger.error(f"Failed to save cache: {e}")

    def add_documents(self, chunks: List[DocumentChunk], embeddings: np.ndarray):
        """Add documents to the vector store"""
        self.chunks.extend(chunks)
        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
        self._save_cache()
        self.logger.info(f"Added {len(chunks)} documents to vector store")

    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[SearchResult]:
        """Search for similar documents"""
        if self.embeddings is None or len(self.chunks) == 0:
            return []

        # Calculate similarities
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]

        # Get top k results
        top_indices = np.argsort(similarities)[-k:][::-1]

        results = []
        for idx in top_indices:
            if similarities[idx] > config.similarity_threshold:
                results.append(
                    SearchResult(chunk=self.chunks[idx], similarity=similarities[idx])
                )

        return results


class PineconeVectorStore(VectorStore):
    """Pinecone vector storage"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            from pinecone import Pinecone

            self.pc = Pinecone(api_key=config.pinecone_api_key)
            self.index = self.pc.Index(config.pinecone_index_name)
            self.logger.info(
                f"Connected to Pinecone index: {config.pinecone_index_name}"
            )
        except ImportError:
            raise ImportError(
                "Pinecone package not found. Install with: pip install pinecone>=3.0.0"
            )
        except Exception as e:
            self.logger.error(f"Failed to connect to Pinecone: {e}")
            raise

    def add_documents(self, chunks: List[DocumentChunk], embeddings: np.ndarray):
        """Add documents to Pinecone"""
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vectors.append(
                {
                    "id": chunk.chunk_id,
                    "values": embedding.tolist(),
                    "metadata": {
                        "text": chunk.content[:1000],  # Limit metadata size
                        "source": chunk.source,
                        "chunk_id": chunk.chunk_id,
                    },
                }
            )

        # Batch upsert
        batch_size = 50
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i : i + batch_size]
            self.index.upsert(vectors=batch)
            time.sleep(0.1)  # Rate limiting

        self.logger.info(f"Added {len(chunks)} documents to Pinecone")

    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[SearchResult]:
        """Search in Pinecone"""
        try:
            response = self.index.query(
                vector=query_embedding.tolist(), top_k=k, include_metadata=True
            )

            results = []
            for match in response["matches"]:
                if match["score"] > config.similarity_threshold:
                    # Handle both 'text' and 'content' metadata keys for backward compatibility
                    content = match["metadata"].get(
                        "text", match["metadata"].get("content", "")
                    )
                    source = match["metadata"].get("source", "unknown")

                    chunk = DocumentChunk(
                        content=content, source=source, chunk_id=match["id"]
                    )
                    results.append(SearchResult(chunk=chunk, similarity=match["score"]))

            return results
        except Exception as e:
            self.logger.error(f"Pinecone search failed: {e}")
            return []


class DocumentProcessor:
    """Handles document loading and processing"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap
        )

    def load_documents(self, directory: Path) -> List[DocumentChunk]:
        """Load documents from directory"""
        chunks = []

        # Load text files
        for txt_file in directory.glob("*.txt"):
            try:
                with open(txt_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if content.strip():
                        file_chunks = self._chunk_document(content, txt_file.name)
                        chunks.extend(file_chunks)
            except Exception as e:
                self.logger.warning(f"Failed to load {txt_file}: {e}")

        # Load PDF files
        try:
            from langchain_community.document_loaders import PyPDFDirectoryLoader

            pdf_loader = PyPDFDirectoryLoader(str(directory))
            pdf_docs = pdf_loader.load()

            for doc in pdf_docs:
                if hasattr(doc, "page_content") and doc.page_content.strip():
                    source = doc.metadata.get("source", "unknown.pdf")
                    file_chunks = self._chunk_document(doc.page_content, source)
                    chunks.extend(file_chunks)
        except Exception as e:
            self.logger.warning(f"Failed to load PDFs: {e}")

        self.logger.info(f"Loaded {len(chunks)} document chunks from {directory}")
        return chunks

    def _chunk_document(self, content: str, source: str) -> List[DocumentChunk]:
        """Split document into chunks"""
        text_chunks = self.text_splitter.split_text(content)

        chunks = []
        for i, chunk_text in enumerate(text_chunks):
            if chunk_text.strip():
                chunk_id = (
                    f"{source}_{i}_{hashlib.md5(chunk_text.encode()).hexdigest()[:8]}"
                )
                chunks.append(
                    DocumentChunk(
                        content=chunk_text.strip(), source=source, chunk_id=chunk_id
                    )
                )

        return chunks


class RAGSystem:
    """Main RAG system class"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.embedding_manager = EmbeddingManager()
        self.vector_store = self._initialize_vector_store()
        self.document_processor = DocumentProcessor()
        self.llm = self._initialize_llm()

        self.system_prompt = """You are a University Course Information Assistant for Texas A&M University's CSCE (Computer Science & Engineering) and ECEN (Electrical & Computer Engineering) departments.

Your responsibilities:
- Provide accurate, reliable information about graduate-level courses and programs
- Base responses exclusively on the provided context from official documents
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

    def _initialize_vector_store(self) -> VectorStore:
        """Initialize vector store based on configuration"""
        if config.use_pinecone:
            try:
                return PineconeVectorStore()
            except Exception as e:
                self.logger.error(
                    f"Failed to initialize Pinecone, falling back to local storage: {e}"
                )
                return LocalVectorStore(config.cache_dir)
        else:
            return LocalVectorStore(config.cache_dir)

    def _initialize_llm(self):
        """Initialize the language model"""
        try:
            genai.configure(api_key=config.gemini_api_key)
            model = genai.GenerativeModel(config.gemini_model)
            self.logger.info(f"Initialized {config.gemini_model}")
            return model
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini: {e}")
            raise

    def index_documents(self, force_reindex: bool = False):
        """Index documents from the data directory"""
        # Check if already indexed (for local storage)
        if not force_reindex and isinstance(self.vector_store, LocalVectorStore):
            if len(self.vector_store.chunks) > 0:
                self.logger.info(
                    "Documents already indexed. Use force_reindex=True to reindex."
                )
                return

        # Load documents
        chunks = self.document_processor.load_documents(config.data_dir)
        if not chunks:
            raise ValueError(f"No documents found in {config.data_dir}")

        # Generate embeddings
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedding_manager.encode(texts)

        # Add to vector store
        self.vector_store.add_documents(chunks, embeddings)
        self.logger.info(f"Successfully indexed {len(chunks)} document chunks")

    def query(self, question: str) -> str:
        """Process a query and return a response"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_manager.encode([question])[0]

            # Search for relevant documents
            results = self.vector_store.search(query_embedding, k=config.max_results)

            if not results:
                return self._generate_no_context_response()

            # Prepare context
            context_parts = []
            for result in results:
                context_parts.append(
                    f"Source: {result.chunk.source}\nContent: {result.chunk.content}"
                )

            context = "\n\n---\n\n".join(context_parts)

            # Generate response
            prompt = f"""{self.system_prompt}

CONTEXT INFORMATION:
{context}

STUDENT QUESTION: {question}

Please provide a comprehensive and helpful response based on the context information above. Include specific details like course numbers, credit hours, prerequisites, and requirements when available."""

            response = self.llm.generate_content(prompt)

            if response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."

        except Exception as e:
            self.logger.error(f"Query processing failed: {e}")
            return f"I encountered an error while processing your question: {str(e)}"

    def _generate_no_context_response(self) -> str:
        """Generate response when no relevant context is found"""
        return """I don't have specific information about that topic in my current database.

For the most accurate and up-to-date information about Texas A&M University courses and programs, I recommend:
- Checking the official Texas A&M course catalog
- Contacting the CSCE or ECEN department directly
- Speaking with an academic advisor

Is there anything else about the available course information I can help you with?"""


# Compatibility class for existing app.py
class AggieeRag:
    """Compatibility wrapper for existing Flask app"""

    def __init__(self):
        self.rag_system = RAGSystem()
        self.messages = [SystemMessage(content=self.rag_system.system_prompt)]

        # Auto-index documents if data directory exists
        if config.data_dir.exists():
            try:
                self.rag_system.index_documents()
            except Exception as e:
                logging.getLogger(__name__).warning(
                    f"Failed to auto-index documents: {e}"
                )

    def augment_prompt(self, query: str) -> str:
        """Process query and return response"""
        return self.rag_system.query(query)


if __name__ == "__main__":
    # Test the system
    try:
        rag = RAGSystem()

        # Index documents
        rag.index_documents()

        # Test queries
        test_queries = [
            "What are the requirements for MS in Computer Science?",
            "Tell me about CSCE 629",
            "What prerequisites does the Deep Learning course have?",
        ]

        for query in test_queries:
            print(f"\n📝 Query: {query}")
            response = rag.query(query)
            print(f"🤖 Response: {response}")
            print("-" * 50)

    except Exception as e:
        logging.getLogger(__name__).error(f"System test failed: {e}")
