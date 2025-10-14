# 🛠️ Setup Instructions - Knowledge Base Search Engine

Complete setup guide for the Knowledge Base Search Engine project.

## 📦 System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 2GB free
- **Internet**: Required for downloading dependencies and API calls

## 🔧 Installation Steps

### 1. Clone or Download the Repository

```bash
# If you have git
git clone <repository-url>
cd unthinkable

# Or download and extract the ZIP file
```

### 2. Verify Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Should show Python 3.8 or higher
```

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Use Homebrew: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

### 3. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 4. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- FastAPI (Web framework)
- Uvicorn (ASGI server)
- Sentence Transformers (Embeddings)
- FAISS (Vector search)
- OpenAI (LLM API)
- PyPDF2 & pdfplumber (PDF parsing)
- And other dependencies...

**Note**: Installation may take 5-10 minutes depending on your internet speed.

### 5. Configure Environment Variables

```bash
# Go back to project root
cd ..

# Copy the example environment file
cp .env.example .env
```

**Edit `.env` file** and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**How to get an OpenAI API key:**
1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new secret key
5. Copy and paste it into your `.env` file

**Important**: Never commit `.env` file to Git!

### 6. Verify Installation

```bash
cd backend
python -c "import fastapi, sentence_transformers, faiss, openai; print('All imports successful!')"
```

If you see "All imports successful!", you're ready to go!

## 🚀 Running the Application

### Option 1: Use Startup Scripts

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Start

```bash
# Activate virtual environment first
cd backend
python main.py
```

The server will start at `http://localhost:8000`

You should see output like:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Opening the Frontend

**Option A: Direct File Open**
- Navigate to `frontend/` folder
- Double-click `index.html`
- Opens in your default browser

**Option B: Local Server (Recommended)**
```bash
# In a new terminal
cd frontend
python -m http.server 8080
```
Then open: `http://localhost:8080`

## 🧪 Testing the Installation

### 1. Test API Endpoints

Open your browser and visit:
- http://localhost:8000 - API information
- http://localhost:8000/health - Health check
- http://localhost:8000/docs - Interactive API documentation (Swagger UI)

### 2. Test with Sample Documents

```bash
cd backend
python test_api.py
```

This will:
- Upload sample documents
- Run multiple test queries
- Display results
- Show pass/fail status

### 3. Manual Test via Frontend

1. Open `frontend/index.html`
2. Upload sample documents from `sample_documents/` folder
3. Ask a question like "What is machine learning?"
4. Verify you get a relevant answer with sources

## ⚙️ Configuration Options

Edit `.env` file to customize:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# OpenAI Configuration
OPENAI_API_KEY=your_key_here
LLM_MODEL=gpt-3.5-turbo  # or gpt-4
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=500

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Retrieval Settings
TOP_K_RESULTS=3
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# File Upload Limits
MAX_UPLOAD_SIZE=100  # MB
```

## 🔍 Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

### Issue: "Port already in use"

**Solution:**
```bash
# Change port in .env file
API_PORT=8001

# Or kill the process using the port
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Issue: OpenAI API errors

**Possible causes:**
1. Invalid API key
   - Check `.env` file for typos
   - Verify key is active on OpenAI dashboard

2. No credits
   - Check your OpenAI account balance
   - Add payment method if needed

3. Rate limiting
   - Wait a few minutes and try again
   - Consider upgrading your OpenAI plan

**Fallback:** The system will use extractive summarization if OpenAI API fails.

### Issue: PDF parsing fails

**Solution:**
- Ensure PDF is not encrypted
- Check if PDF contains text (not scanned images)
- Try a different PDF file
- Check backend logs for specific errors

### Issue: Frontend can't connect to backend

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check browser console for CORS errors
3. Ensure correct API_URL in `frontend/index.html` (line with `const API_URL`)
4. Try disabling browser extensions
5. Use Chrome/Firefox (better CORS handling)

### Issue: Slow performance

**Solutions:**
- Reduce `CHUNK_SIZE` in `.env`
- Use smaller documents
- Reduce `TOP_K_RESULTS`
- Use faster embedding model
- Ensure adequate RAM available

## 🔒 Security Best Practices

1. **Never commit `.env` file**
   - Already in `.gitignore`
   - Don't share API keys publicly

2. **Use environment variables**
   - Keep sensitive data in `.env`
   - Don't hardcode credentials

3. **Update dependencies regularly**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

4. **For production deployment:**
   - Use HTTPS
   - Add authentication
   - Implement rate limiting
   - Use secrets management (AWS Secrets Manager, etc.)
   - Set up monitoring and logging

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend                         │
│         (HTML/CSS/JavaScript - Client Side)         │
└───────────────────┬─────────────────────────────────┘
                    │ HTTP/REST API
                    ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │   main   │  │   rag    │  │ document │         │
│  │   .py    │  │   .py    │  │ _utils.py│         │
│  └──────────┘  └──────────┘  └──────────┘         │
└───────────────────┬─────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌─────────────┐ ┌────────┐ ┌──────────┐
│ Sentence    │ │ FAISS  │ │ OpenAI   │
│ Transformers│ │ Vector │ │ GPT API  │
│ (Embeddings)│ │ Store  │ │ (LLM)    │
└─────────────┘ └────────┘ └──────────┘
```

## 🎓 Learning Resources

### Understanding RAG
- [What is RAG?](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### Embeddings & Vector Search
- [Sentence Transformers](https://www.sbert.net/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)

### OpenAI API
- [OpenAI Documentation](https://platform.openai.com/docs/)
- [GPT Best Practices](https://platform.openai.com/docs/guides/gpt-best-practices)

## 🆘 Getting Help

1. **Check logs**: Backend logs show detailed error messages
2. **Review documentation**: README.md and DEMO_GUIDE.md
3. **Test with sample documents**: Verify basic functionality
4. **Search for similar issues**: Check GitHub issues (if public repo)
5. **Create an issue**: Provide details about your problem

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created and configured with OpenAI API key
- [ ] Backend starts successfully (`python main.py`)
- [ ] Can access http://localhost:8000/docs
- [ ] Frontend opens in browser
- [ ] Can upload sample documents
- [ ] Can query and get responses
- [ ] Test script runs successfully

## 🎉 Next Steps

Once setup is complete:
1. ✅ Upload your own documents
2. ✅ Experiment with different queries
3. ✅ Explore the API documentation at `/docs`
4. ✅ Customize configuration in `.env`
5. ✅ Review the code to understand the architecture
6. ✅ Record your demo video
7. ✅ Share with others!

---

**Need help? Check the troubleshooting section or review the logs for detailed error messages.**
