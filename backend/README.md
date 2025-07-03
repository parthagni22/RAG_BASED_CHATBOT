# Aggie Course Navigator 🎓

A Retrieval-Augmented Generation (RAG) system designed to help Texas A&M University students navigate CSCE (Computer Science & Engineering) and ECEN (Electrical & Computer Engineering) course information using AI-powered conversational interface.

## 🌟 Features

### Core Capabilities
- **Intelligent Course Search**: Semantic search through course catalogs, syllabi, and degree requirements
- **AI-Powered Responses**: Context-aware answers using Google's Gemini AI model
- **Multi-Format Support**: Process both text files and PDF documents
- **Flexible Storage**: Choose between local vector storage or cloud-based Pinecone
- **Real-time Chat**: Interactive web interface with React frontend

### Technical Features
- **Multiple Embedding Providers**: OpenAI embeddings or free SentenceTransformers
- **Smart Caching**: Automatic caching for improved performance
- **Document Chunking**: Intelligent text splitting for optimal retrieval
- **Health Monitoring**: Built-in system monitoring and statistics
- **Error Handling**: Comprehensive error handling and logging
- **CORS Support**: Ready for frontend integration

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │────│   Flask API     │────│   RAG System    │
│                 │    │                 │    │                 │
│ - Chat Interface│    │ - /llmtrigger   │    │ - Doc Processing│
│ - Course Search │    │ - /health       │    │ - Vector Search │
│ - User Interface│    │ - /api/stats    │    │ - AI Generation │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ├─────────────────┬─────────────────┐
                                │                 │                 │
                        ┌───────▼──────┐ ┌────────▼────────┐ ┌─────▼──────┐
                        │   Gemini AI  │ │ Vector Storage  │ │ Documents  │
                        │              │ │                 │ │            │
                        │ - Response   │ │ - Local/Pinecone│ │ - Database/│
                        │   Generation │ │ - Embeddings    │ │ - Text/PDF │
                        └──────────────┘ └─────────────────┘ └────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js (for React frontend)
- Google Gemini API key (free)
- UV or pip for package management

### Installation

1. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd aggie-course-navigator
   ```

2. **Backend Setup**
   ```bash
   cd backend

   # Option 1: Using UV (recommended)
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt

   # Option 2: Using pip
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and add your API keys
   # At minimum, you need a Gemini API key
   ```

4. **Create Sample Data (Optional)**
   ```bash
   python setup.py
   ```
   This will create sample course data and initialize directories.

5. **Start the Backend**
   ```bash
   python app.py
   ```
   Server runs on `http://localhost:8080`

6. **Frontend Setup**
   ```bash
   cd frontend
   npm install

   # Copy frontend environment file
   cp .env.example .env

   # Start the frontend
   npm run dev
   ```

## 📁 Project Structure

```
aggie-course-navigator/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── rag_system.py         # Core RAG system implementation
│   ├── config.py             # Configuration management
│   ├── setup.py              # Automated setup script
│   ├── .env                  # Environment variables (create from .env.example)
│   ├── .env.example          # Example environment file
│   ├── .gitignore
│   ├── requirements.txt      # Python dependencies
│   ├── Database/            # Course documents directory
│   │   ├── csce_629_algorithms.txt
│   │   ├── csce_636_deep_learning.txt
│   │   └── ms_degree_requirements.txt
│   ├── cache/              # Vector embeddings cache
│   └── logs/               # Application logs
├── frontend/               # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── .env.example
│   └── .env
└── README.md
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required: API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Enhanced features
PINECONE_API_KEY=your_pinecone_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
DEBUG=true
HOST=0.0.0.0
PORT=8080

# Vector Storage: 'local' or 'pinecone'
VECTOR_STORAGE=local

# Embedding Model: 'sentence-transformers' or 'openai'
EMBEDDING_MODEL=sentence-transformers
```

### Getting API Keys

1. **Gemini API Key** (Required, Free):
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add to your `.env` file

2. **Pinecone API Key** (Optional, for cloud storage):
   - Sign up at [Pinecone](https://app.pinecone.io/)
   - Create a new project
   - Get your API key from the dashboard

3. **OpenAI API Key** (Optional, for better embeddings):
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Note: This is a paid service

## 🛠️ API Endpoints

### Core Endpoints
- `POST /llmtrigger` - Main chat endpoint
- `GET /health` - System health check
- `GET /api/stats` - Detailed system statistics
- `GET /api/test` - API test endpoint
- `POST /api/reindex` - Reindex documents

### Request/Response Format
```javascript
// Chat Request
POST /llmtrigger
{
  "message": "What are the prerequisites for CSCE 629?"
}

// Response
{
  "message": "CSCE 629 - Analysis of Algorithms requires CSCE 221 (Data Structures & Algorithms) and CSCE 222 (Discrete Structures) as prerequisites..."
}
```

## 📊 Usage Examples

### Student Queries
```
"What are the requirements for MS in Computer Science?"
"Tell me about CSCE 636 - Deep Learning"
"What prerequisites does the algorithms course have?"
"How many credit hours is the Computer Vision course?"
"What research areas are available for graduate students?"
```

### System Responses
The system provides detailed, contextual answers including:
- Course numbers and credit hours
- Prerequisites and corequisites
- Degree requirements and specializations
- Grading policies and project information
- Research areas and faculty information

## 🔍 Monitoring and Maintenance

### Health Check
```bash
curl http://localhost:8080/health
```

### System Statistics
```bash
curl http://localhost:8080/api/stats
```

### Reindex Documents
```bash
curl -X POST http://localhost:8080/api/reindex
```

## 📚 Adding New Course Data

1. **Add Documents**: Place new `.txt` or `.pdf` files in `backend/Database/` directory
2. **Reindex**: The system will automatically detect and index new files
3. **Manual Reindex**: Use `/api/reindex` endpoint if needed

### Document Format Guidelines
- Use clear section headers
- Include course numbers and credit hours
- Specify prerequisites clearly
- Add comprehensive course descriptions
- Include grading policies and requirements

## 🚨 Troubleshooting

### Common Issues

**1. API Key Errors**
```
Error: Gemini API key is required
Solution: Check .env file and ensure GEMINI_API_KEY is set
```

**2. No Documents Found**
```
Error: No documents found in Database/
Solution: Add .txt or .pdf files to backend/Database/ directory
```

**3. Port Already in Use**
```
Error: Port 8080 is already in use
Solution: Change PORT in .env file or kill existing process
```

**4. Virtual Environment Issues**
```
Error: Module not found
Solution: Ensure virtual environment is activated:
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### Debug Mode
Enable debug mode in your `.env` file:
```bash
DEBUG=true
```

## 🔐 Security Considerations

- **API Keys**: Never commit `.env` files to version control
- **CORS**: Configure CORS_ORIGINS for production
- **Input Validation**: System validates query length and content
- **Rate Limiting**: Consider implementing rate limiting for production

## 📈 Performance Optimization

### For Large Document Sets
- Use Pinecone for cloud-based vector storage
- Enable OpenAI embeddings for better quality
- Adjust CHUNK_SIZE based on document type
- Monitor memory usage and optimize accordingly

### Caching Strategy
- Local vector storage automatically caches embeddings
- Pinecone provides cloud-based persistent storage
- Clear cache when updating documents significantly

## 🧪 Testing

### Test the Backend
```bash
cd backend
source .venv/bin/activate
python -c "
from rag_system import RAGSystem
rag = RAGSystem()
rag.index_documents()
response = rag.query('What courses are available?')
print(response)
"
```

### API Testing
```bash
# Test health endpoint
curl http://localhost:8080/health

# Test chat endpoint
curl -X POST http://localhost:8080/llmtrigger \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about computer science courses"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini**: For the powerful language model
- **Sentence Transformers**: For free, high-quality embeddings
- **Pinecone**: For cloud vector database services
- **LangChain**: For document processing utilities
- **Texas A&M University**: For course information and academic data

## 📞 Support

Create an issue with detailed error information for support.