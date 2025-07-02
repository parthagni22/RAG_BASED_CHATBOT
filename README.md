# Texas A&M Course Guide - RAG-Based Chatbot

A specialized AI-powered chatbot designed to help CSCE (Computer Science & Engineering) and ECEN (Electrical & Computer Engineering) students at Texas A&M University navigate course information, degree requirements, and academic policies.

## 🎯 Features

- **Intelligent Q&A**: Get instant answers about courses, prerequisites, and degree requirements
- **Semantic Search**: Uses advanced embeddings to find relevant information
- **Real-time Responses**: Powered by Google Gemini for natural language generation
- **Scalable Architecture**: Built with Pinecone vector database for efficient retrieval
- **Easy to Extend**: Simply add more documents to expand knowledge base

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Flask     │────▶│   RAG Core    │────▶│   Gemini    │
│   Web UI    │      │   (Search)   │      │   (Gen AI)  │
└─────────────┘      └──────────────┘      └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Pinecone   │
                    │ Vector DB   │
                    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- Free API keys from:
  - [Google AI Studio](https://aistudio.google.com/app/apikey) (Gemini)
  - [Pinecone](https://www.pinecone.io/) (Vector Database)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/RAG_BASED_CHATBOT.git
cd RAG_BASED_CHATBOT
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up API keys**

Create/edit `Data/keys.txt`:
```json
{
    "pinecone": "your-pinecone-api-key-here",
    "gemini": "your-gemini-api-key-here",
    "openai": ""
}
```

5. **Create Pinecone Index**
- Go to [Pinecone Console](https://app.pinecone.io/)
- Create a new index with:
  - Name: `indianconsti`
  - Dimensions: `384`
  - Metric: `cosine`
  - Cloud: `AWS`
  - Region: `us-east-1`

6. **Add course data**
```bash
python create_simple_data.py
```

7. **Generate embeddings**
```bash
python AggieCourses.py
```

8. **Run the application**
```bash
python app.py
```

9. **Access the chatbot**
Open your browser and go to: `http://127.0.0.1:5000`

## 📁 Project Structure

```
RAG_BASED_CHATBOT/
├── app.py                  # Flask application entry point
├── AggieCourses.py         # RAG implementation with Pinecone
├── requirements.txt        # Python dependencies
├── Data/
│   └── keys.txt           # API keys configuration
├── Database/              # Course information files
│   ├── course_1_*.txt
│   └── ...
├── templates/
│   └── AggieCourses.html  # Web interface
├── src/
│   └── utils.py           # Utility functions
└── README.md              # This file
```

## 🔧 Configuration

### API Keys Setup

1. **Gemini API Key** (Free)
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Click "Get API Key"
   - Copy and paste into `Data/keys.txt`

2. **Pinecone API Key** (Free tier available)
   - Sign up at [Pinecone](https://www.pinecone.io/)
   - Go to API Keys section
   - Create new API key
   - Copy and paste into `Data/keys.txt`

### Customization Options

- **Embedding Model**: Currently uses `all-MiniLM-L6-v2` (384 dimensions)
- **LLM Model**: Uses `gemini-1.5-flash` for responses
- **Chunk Size**: 800 characters with 50 character overlap
- **Search Results**: Returns top 3 most relevant chunks

## 📚 Adding More Knowledge

### Method 1: Add Text Files
Create `.txt` files in the `Database/` folder:
```text
Course Title

Course content, prerequisites, descriptions...
```

### Method 2: Add PDF Files
Simply place PDF files in the `Database/` folder

### Method 3: Bulk Import
```bash
python create_more_courses.py  # Creates additional sample courses
```

After adding new content:
```bash
python AggieCourses.py  # Regenerate embeddings
python app.py           # Restart the application
```

## 💬 Example Queries

- "Tell me about CSCE 629"
- "What are the prerequisites for Deep Learning?"
- "Explain the MS degree requirements"
- "What's the difference between thesis and non-thesis options?"
- "How many credit hours do I need for a PhD?"

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
```bash
pip install --upgrade -r requirements.txt
```

2. **Pinecone Connection Error**
- Verify API key is correct
- Check index name is exactly `indianconsti`
- Ensure index dimensions are `384`

3. **Gemini API Error**
- Verify API key is valid
- Check for typos in `Data/keys.txt`
- Ensure no rate limiting

4. **No Results Found**
- Run `python AggieCourses.py` to generate embeddings
- Lower similarity threshold in `search_similar_chunks()`

### Debug Mode
```bash
python check_pinecone.py  # Verify Pinecone setup
python test_gemini_key.py # Test Gemini API
```

## 🚀 Deployment

### Local Deployment
The application runs locally by default on `http://127.0.0.1:5000`

### Heroku Deployment
1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy:
```bash
heroku create your-app-name
heroku config:set PINECONE_API_KEY=your-key
heroku config:set GEMINI_API_KEY=your-key
git push heroku main
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📈 Future Enhancements

- [ ] Add more course data and department information
- [ ] Implement conversation history
- [ ] Add multi-language support
- [ ] Create admin interface for content management
- [ ] Add analytics dashboard
- [ ] Implement caching for faster responses
- [ ] Add voice input/output capabilities

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Texas A&M University for course information
- Google for Gemini API
- Pinecone for vector database
- OpenAI for embeddings inspiration
- The open-source community

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Email: your.email@example.com

---

**Note**: This project is for educational purposes and is not officially affiliated with Texas A&M University.