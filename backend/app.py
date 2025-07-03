#!/usr/bin/env python3
"""
Fixed Flask application with working routes (no duplicates)
"""

import logging
import traceback
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from config import config, config_manager
from rag_system import AggieeRag


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change in production

    # Enable CORS for development
    # CORS(app)
    CORS(app, origins=[
        "http://localhost:5173",  # Vite dev server ← This one!
        "http://127.0.0.1:5173"   # ← And this one!
    ])

    # Validate configuration
    is_valid, issues = config_manager.validate_config()
    if not is_valid:
        logger.error("Configuration validation failed:")
        for issue in issues:
            logger.error(f"  - {issue}")
        raise RuntimeError("Invalid configuration. Please fix the issues above.")

    # Initialize RAG system
    try:
        rag_system = AggieeRag()
        logger.info("RAG system initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")
        raise

    @app.route('/')
    def index():
        """Serve the main chat interface"""
        try:
            return render_template("AggieCourses.html")
        except Exception as e:
            logger.error(f"Error serving index page: {e}")
            return jsonify({"error": "Failed to load page"}), 500

    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        try:
            # Get document count safely
            doc_count = "Unknown"
            vector_store_type = "Unknown"

            try:
                if hasattr(rag_system, 'rag_system') and hasattr(rag_system.rag_system, 'vector_store'):
                    vector_store = rag_system.rag_system.vector_store
                    vector_store_type = "Pinecone" if hasattr(vector_store, 'pc') else "Local"

                    if hasattr(vector_store, 'chunks'):
                        doc_count = len(vector_store.chunks)
                    elif hasattr(vector_store, 'index'):
                        try:
                            pinecone_stats = vector_store.index.describe_index_stats()
                            doc_count = pinecone_stats.get('total_vector_count', 'Unknown')
                        except:
                            doc_count = "Pinecone Connected"
            except Exception as e:
                logger.warning(f"Could not get document count: {e}")

            stats = {
                "status": "healthy",
                "message": "Aggie Course Navigator is running successfully!",
                "version": "2.0",
                "vector_store": vector_store_type,
                "embedding_provider": "openai" if config.openai_api_key else "sentence_transformers",
                "gemini_model": config.gemini_model,
                "documents_indexed": doc_count,
                "api_keys_configured": {
                    "gemini": bool(config.gemini_api_key),
                    "pinecone": bool(config.pinecone_api_key),
                    "openai": bool(config.openai_api_key)
                },
                "timestamp": "2025-07-03"
            }
            return jsonify(stats)
        except Exception as e:
            logger.error(f"Error in health check: {e}")
            return jsonify({
                "status": "unhealthy",
                "error": str(e),
                "version": "2.0",
                "message": "Health check failed"
            }), 500

    @app.route('/api/stats')
    def get_stats():
        """Get detailed system statistics"""
        try:
            # Get document count safely
            doc_count = "N/A"
            vector_store_type = "Unknown"

            try:
                if hasattr(rag_system, 'rag_system') and hasattr(rag_system.rag_system, 'vector_store'):
                    vector_store = rag_system.rag_system.vector_store
                    vector_store_type = "Pinecone" if hasattr(vector_store, 'pc') else "Local"

                    if hasattr(vector_store, 'chunks'):
                        doc_count = len(vector_store.chunks)
                    elif hasattr(vector_store, 'index'):
                        try:
                            pinecone_stats = vector_store.index.describe_index_stats()
                            doc_count = pinecone_stats.get('total_vector_count', 'Unknown')
                        except:
                            doc_count = "Connected to Pinecone"
            except Exception as e:
                logger.warning(f"Could not get stats: {e}")

            stats = {
                "system_info": {
                    "name": "Aggie Course Navigator",
                    "status": "operational",
                    "version": "2.0.0",
                    "uptime": "Running"
                },
                "vector_storage": {
                    "type": vector_store_type,
                    "total_documents": doc_count,
                    "embedding_model": config.embedding_model,
                    "embedding_dimensions": "384 (SentenceTransformers)" if not config.openai_api_key else "1536 (OpenAI)"
                },
                "ai_models": {
                    "llm": config.gemini_model,
                    "embedding_provider": "SentenceTransformers" if not config.openai_api_key else "OpenAI"
                },
                "configuration": {
                    "chunk_size": config.chunk_size,
                    "chunk_overlap": config.chunk_overlap,
                    "max_results": config.max_results,
                    "similarity_threshold": config.similarity_threshold
                },
                "api_status": {
                    "gemini_configured": bool(config.gemini_api_key),
                    "pinecone_configured": bool(config.pinecone_api_key),
                    "openai_configured": bool(config.openai_api_key)
                }
            }
            return jsonify(stats)
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return jsonify({
                "error": "Failed to get statistics",
                "details": str(e),
                "system_info": {
                    "status": "error",
                    "version": "2.0.0"
                }
            }), 500

    @app.route('/api/test')
    def test_endpoint():
        """Test endpoint to verify API is working"""
        return jsonify({
            "message": "API test successful!",
            "status": "success",
            "system": "Aggie Course Navigator",
            "available_endpoints": [
                "GET /health - System health check",
                "GET /api/stats - Detailed system statistics",
                "GET /api/test - This test endpoint",
                "POST /api/reindex - Reindex documents",
                "POST /llmtrigger - Chat with AI"
            ],
            "timestamp": "2025-07-03"
        })

    @app.route('/llmtrigger', methods=['POST'])
    def process_query():
        """Process user queries and return AI responses"""
        try:
            # Validate request
            if request.method != 'POST':
                return jsonify({"error": "Method not allowed"}), 405

            # Get message from form data or JSON
            if request.is_json:
                data = request.get_json()
                query = data.get('message', '').strip()
            else:
                query = request.form.get('message', '').strip()

            if not query:
                return jsonify({"error": "No message provided"}), 400

            if len(query) > 2000:  # Reasonable limit
                return jsonify({"error": "Message too long"}), 400

            logger.info(f"Processing query: {query[:100]}...")

            # Process query with RAG system
            response = rag_system.augment_prompt(query)

            if not response:
                response = "I apologize, but I couldn't generate a response. Please try again."

            logger.info(f"Generated response length: {len(response)}")

            return jsonify({"message": response})

        except ValueError as e:
            logger.warning(f"Invalid request: {e}")
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            logger.error(traceback.format_exc())
            return jsonify({
                "error": "An internal error occurred. Please try again.",
                "message": "I apologize, but I encountered an error while processing your request. Please try again."
            }), 500

    @app.route('/api/reindex', methods=['POST'])
    def reindex_documents():
        """Reindex documents (admin endpoint)"""
        try:
            rag_system.rag_system.index_documents(force_reindex=True)
            return jsonify({"message": "Documents reindexed successfully"})
        except Exception as e:
            logger.error(f"Error reindexing documents: {e}")
            return jsonify({"error": "Failed to reindex documents"}), 500

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            "error": "Not found",
            "message": "Endpoint not available",
            "available_endpoints": ["/health", "/api/stats", "/api/test", "/llmtrigger"]
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error"}), 500

    return app


# Create the app instance
application = create_app()
app = application  # For compatibility


if __name__ == "__main__":
    try:
        logger.info(f"Starting Flask application on {config.host}:{config.port}")
        logger.info(f"Debug mode: {config.debug}")
        logger.info(f"Vector store: {'Pinecone' if config.use_pinecone else 'Local'}")

        app.run(
            host=config.host,
            port=8080,
            debug=config.debug
        )
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise