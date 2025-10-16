# 🎬 Demo Guide - Knowledge Base Search Engine

https://drive.google.com/file/d/1tJnmg2W19jJb4JndgArUeLN1pXgWdsmv/view
This guide will walk you through a complete demonstration of the Knowledge Base Search Engine.

## 📋 Prerequisites

Before starting the demo, ensure you have:
- ✅ Python 3.8+ installed
- ✅ All dependencies installed (`pip install -r backend/requirements.txt`)
- ✅ OpenAI API key configured in `.env` file
- ✅ Backend server running

## 🚀 Quick Start Demo

### Step 1: Start the Backend Server

```bash
# On Windows
start.bat

# On Mac/Linux
./start.sh

# Or manually
cd backend
python main.py
```

The server should start at `http://localhost:8000`

### Step 2: Open the Frontend

Open `frontend/index.html` in your web browser, or serve it:

```bash
cd frontend
python -m http.server 8080
```

Navigate to `http://localhost:8080`

### Step 3: Upload Sample Documents

**Option A: Using the Web Interface**
1. Click "Select Files" or drag & drop files
2. Select the sample documents from `sample_documents/` folder:
   - `machine_learning_basics.txt`
   - `data_science_intro.txt`
3. Click "Upload Selected Files"
4. Wait for confirmation (should show number of chunks processed)

**Option B: Using cURL**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "files=@sample_documents/machine_learning_basics.txt" \
  -F "files=@sample_documents/data_science_intro.txt"
```

### Step 4: Ask Questions

Try these sample queries:

#### Query 1: Basic Question
**Question:** "What is machine learning?"

**Expected Output:**
- Clear definition of machine learning
- Reference to AI and data-driven decision making
- Sources cited from uploaded documents

#### Query 2: Specific Topic
**Question:** "Explain supervised learning and give examples"

**Expected Output:**
- Definition of supervised learning
- Examples like classification and regression
- Popular algorithms mentioned

#### Query 3: Comparison Question
**Question:** "What is the difference between supervised and unsupervised learning?"

**Expected Output:**
- Explanation of both types
- Key differences highlighted
- Use cases for each

#### Query 4: Process Question
**Question:** "What are the steps in the data science process?"

**Expected Output:**
- List of data science process steps
- Brief explanation of each step
- Tools mentioned

#### Query 5: Technical Details
**Question:** "What evaluation metrics are used for classification problems?"

**Expected Output:**
- List of metrics (accuracy, precision, recall, F1-score)
- Brief explanation of when to use each
- Sources from relevant document sections

## 🎥 Recording Your Demo Video

### Suggested Demo Flow (5-10 minutes)

**Part 1: Introduction (1 minute)**
- Show the landing page
- Explain the purpose: RAG-based knowledge search
- Highlight key features

**Part 2: Document Upload (2 minutes)**
- Demonstrate drag & drop functionality
- Upload sample documents
- Show processing confirmation
- Point out document count updates

**Part 3: Querying (5 minutes)**
- Ask 3-4 diverse questions
- Show how answers are synthesized
- Highlight source citations
- Demonstrate different query types:
  - Factual questions
  - Explanation requests
  - Comparison queries

**Part 4: Technical Overview (2 minutes)**
- Briefly show the backend code structure
- Explain RAG pipeline:
  - Document chunking
  - Embedding generation
  - FAISS vector search
  - LLM synthesis
- Show API endpoints in browser/Postman

**Part 5: Conclusion (1 minute)**
- Summarize capabilities
- Mention scalability and extensibility
- Show GitHub repository

### Recording Tips

1. **Preparation**
   - Clear browser cache
   - Close unnecessary tabs/applications
   - Test everything beforehand
   - Prepare your script

2. **Recording Setup**
   - Use screen recording software (OBS, Loom, QuickTime)
   - Record at 1080p resolution
   - Enable microphone for narration
   - Use a quiet environment

3. **Presentation**
   - Speak clearly and at moderate pace
   - Pause between major steps
   - Show real results (don't fake responses)
   - Handle errors gracefully if they occur

4. **Editing**
   - Trim unnecessary parts
   - Add text overlays for key points
   - Include background music (optional)
   - Add intro/outro slides

## 🧪 Testing Scenarios

### Scenario 1: Empty Knowledge Base
1. Clear all documents
2. Try to query
3. Show error message: "No documents in knowledge base"
4. Upload documents
5. Query successfully

### Scenario 2: Multiple Document Types
1. Upload both TXT and PDF files
2. Query across all documents
3. Show sources from different files

### Scenario 3: API Testing
```bash
# Test with cURL
curl http://localhost:8000/health
curl http://localhost:8000/documents
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?", "top_k": 3}'
```

### Scenario 4: Performance Test
1. Upload larger documents
2. Show quick response times
3. Demonstrate concurrent queries

## 📊 Key Metrics to Highlight

1. **Processing Speed**
   - Document upload and chunking time
   - Query response time (< 2 seconds)

2. **Retrieval Quality**
   - Relevance of retrieved chunks
   - Accuracy of answers
   - Proper source citations

3. **User Experience**
   - Intuitive interface
   - Clear error messages
   - Responsive design

4. **Technical Excellence**
   - Clean code structure
   - RESTful API design
   - Proper error handling

## 🎯 Demo Script Example

```
[Opening]
"Hello! Today I'm demonstrating a Knowledge Base Search Engine built with 
Retrieval-Augmented Generation (RAG). This system allows you to upload 
documents and ask questions to get AI-powered answers with source citations."

[Upload Demo]
"Let me start by uploading some documents about machine learning and data 
science. I can either drag and drop files or click to browse. The system 
processes PDFs and text files, chunks them intelligently, and creates 
embeddings for semantic search."

[Show processing]
"As you can see, the documents are being processed... and now we have 
[X] chunks indexed in our knowledge base."

[Query Demo]
"Now let's ask some questions. First, a basic one: 'What is machine learning?'"
[Show result]
"Notice how the system provides a clear, synthesized answer pulling from 
relevant sections of our documents. The sources are cited below with 
relevance scores."

[More queries]
"Let me try a more complex question..."
[Continue with 2-3 more queries]

[Technical Overview]
"Under the hood, this system uses:
- Sentence transformers for embeddings
- FAISS for efficient vector similarity search
- OpenAI's GPT for answer synthesis
- FastAPI for the backend REST API"

[Closing]
"The system is production-ready, well-documented, and extensible. 
Check out the GitHub repository for full source code and documentation. 
Thank you for watching!"
```

## 📝 Common Issues During Demo

### Issue: Server not responding
**Solution:** 
```bash
# Check if server is running
curl http://localhost:8000/health

# Restart if needed
cd backend
python main.py
```

### Issue: Upload fails
**Solution:**
- Check file formats (PDF/TXT only)
- Verify file sizes
- Check server logs for errors

### Issue: No/poor answers
**Solution:**
- Ensure documents are uploaded
- Check OpenAI API key
- Try rephrasing the question
- Verify documents contain relevant information

### Issue: Frontend can't connect
**Solution:**
- Check CORS settings in main.py
- Verify API_URL in frontend/index.html
- Check browser console for errors

## 🎬 Post-Production

1. - Google Drive (with public link)
   - https://drive.google.com/file/d/1tJnmg2W19jJb4JndgArUeLN1pXgWdsmv/view

2. **Add Description**
   ```
   Knowledge Base Search Engine Demo
   
   A RAG-based search engine that allows document upload and 
   AI-powered question answering with source citations.
   
   Tech Stack:
   - Backend: Python, FastAPI
   - RAG: Sentence Transformers, FAISS, OpenAI GPT
   - Frontend: HTML/CSS/JavaScript
   
   GitHub: [Your repo link]
   
   Timestamps:
   0:00 - Introduction
   0:30 - Document Upload
   2:00 - Querying Demo
   5:00 - Technical Overview
   7:00 - Conclusion
   ```

3. **Add to README**
   Update README.md with video link:
   ```markdown
   ## 🎬 Demo Video
   
   Watch the demo: [YouTube Link]
   ```

## ✅ Demo Checklist

Before recording:
- [ ] Backend server running
- [ ] Frontend accessible
- [ ] Sample documents ready
- [ ] .env configured with API key
- [ ] Test all features working
- [ ] Close unnecessary applications
- [ ] Clear browser cache/history
- [ ] Prepare demo script
- [ ] Test recording software

During recording:
- [ ] Show clear, deliberate actions
- [ ] Narrate what you're doing
- [ ] Demonstrate key features
- [ ] Show both successes and handling of edge cases
- [ ] Keep within 5-10 minutes

After recording:
- [ ] Review for quality
- [ ] Edit if needed
- [ ] Add captions/overlays
- [ ] Upload to platform
- [ ] Add link to README
- [ ] Share with stakeholders

---

**Good luck with your demo! 🚀**
