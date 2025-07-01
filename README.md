# RAG_BASED_CHATBOT

A specialized chatbot designed for CSCE (Computer Science & Engineering) and ECEN (Electrical & Computer Engineering) students at Texas A&M University. This chatbot simplifies the process of finding accurate and concise information related to courses, degrees, and credit requirements for students

The bot leverages  **LangChain, GPT-4.o mini, and Pinecone Vector DB** to deliver fast, relevant responses to specific academic queries. By using embeddings and a lightweight model, it improves user experience and helps students avoid the hassle of digging through long course handbooks or scattered online resources

## Features
- **Course, Degree, and Credit Information:** Provides precise and quick answers to frequently asked questions about CSCE and ECEN programs.
- **Interactive AI Experience:** Tailored for student needs, it reduces the time spent on retrieving important academic information.
- **Powered by LangChain and Pinecone:** This bot uses the latest OpenAI technologies for embeddings and response generation.
- **Embeddings:** Uses OpenAI's "text-embedding-ada-002" for generating vector embeddings.
- **Responses:** Utilizes "gpt-3.5-turbo" for providing prompt and relevant answers.
- **Continuous Integration and Deployment:** Implemented CI/CD pipeline using GitHub Actions.
- **Hosting:** Deployed on Heroku, allowing easy access to students anywhere, anytime.

## Installation & Setup
**1. Clone the Repository:**<br>
     ``` 
     git clone https://github.com/pragatinaikare/RAG_BASED_CHATBOT.git
     ```<br>

**2. Install Dependencies:**

```bash
pip install -r requirements.txt
```

**3. Set Up API Keys:** 
You will need to create accounts with Pinecone and OpenAI to get your API keys. Add these keys in keys.txt file inside Data Folder

**4. To Run Locally:**
 Uncomment this line:
    ```python
    app.run(host="0.0.0.0", port=8000, debug=True)
    ```
Comment out the default `app.run()` line.
Run  app.py file
```bash
python app.py
```



