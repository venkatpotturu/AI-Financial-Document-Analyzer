# AI-Financial-Document-Analyzer
# AI Financial Document Analyzer 📊📄

An end-to-end **Streamlit-based AI application** that allows users to upload financial and textual documents and interact with them using a chat interface. The system extracts content from files, converts it into vector embeddings, stores them using FAISS, and retrieves relevant context to generate intelligent responses.

This project demonstrates practical usage of **NLP, embeddings, vector databases, and Streamlit UI**.

---

## 📌 Key Highlights

* Upload financial documents and datasets
* Ask questions in natural language
* Semantic search using embeddings
* Context-aware AI responses
* Clean, lightweight Streamlit UI
* Fully local execution (no cloud dependency)

---

## 🚀 Features

* 📂 File upload support:
    * PDF
    * DOCX
    * TXT
    * CSV
    * XLSX
    * PNG / JPG / JPEG
* 🧠 Embedding-based semantic search
* 🔍 FAISS vector indexing
* 💬 Chat-style question answering
* ⚡ Fast response with cached embeddings
* 🔐 Environment variable support using `.env`

---

## 🛠️ Technology Stack

* **Language:** Python
* **Frontend:** Streamlit
* **Embeddings Model:** SentenceTransformers (\`BAAI/bge-small-en-v1.5\`)
* **Vector Database:** FAISS (CPU)
* **Text Extraction:** PyMuPDF (\`fitz\`)
* **Environment Management:** python-dotenv
* **Core Libraries:** NumPy

---

## 📁 Project Structure

\`\`\`
AI-Financial-Document-Analyzer/
│── app.py # Streamlit application
│── file_extractor.py # Extracts text from files
│── embedder.py # Chunking & FAISS storage
│── chat_engine.py # Retrieval & response generation
│── requirements.txt
│── README.md
│── .gitignore
│── .env # (ignored)
│── venv/ # (ignored)
\`\`\`

---

## ⚙️ Installation & Setup (Complete)

### 1️⃣ Clone the Repository
\`\`\`bash
git clone https://github.com/venkatpotturu/AI-Financial-Document-Analyzer.git
cd AI-Financial-Document-Analyzer
\`\`\`

---

### 2️⃣ Create Virtual Environment

**Windows**
\`\`\`bash
python -m venv venv
venv\Scripts\activate
\`\`\`

**Mac / Linux**
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3️⃣ Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`
If Streamlit command is not recognized:
\`\`\`bash
python -m pip install streamlit
\`\`\`

### 4️⃣ Environment Variables
Create a \`.env\` file (if required):

\`\`\`env
OPENAI_API_KEY=your_api_key_here
\`\`\`
⚠️ **Do not upload \`.env\` to GitHub.**

### 5️⃣ Run the Application
\`\`\`bash
python -m streamlit run app.py
\`\`\`

### Open in browser:
\`http://localhost:8501\`

---

### 🧪 Application Workflow
* User uploads a document
* Text is extracted from the file
* Text is split into chunks
* Chunks are converted into embeddings 
* Embeddings are stored in FAISS
* User query is embedded
* Most relevant chunks are retrieved
* Context-aware response is generated
* Conversation history is maintained

---

### 📊 Use Cases
* Financial document analysis
* Annual report understanding
* Invoice and transaction review
* Bank statement analysis
* Academic document Q&A
* Large document summarization

---

### ❗ Common Issues & Fixes
* **Streamlit not recognized**
    \`\`\`bash
    python -m streamlit run app.py
    \`\`\`
* **FAISS installation issue (Windows)**
    \`\`\`bash
    pip uninstall faiss
    pip install faiss-cpu
    \`\`\`
* **Module not found error**
    * Ensure all \`.py\` files are in the same directory
    * Check correct file names and imports

---

### 🔒 Security Notes
* \`.env\` is excluded via \`.gitignore\`
* No API keys are hardcoded
* Local-only execution

---

## 🔮 Future Enhancements
* OCR for scanned documents
* Multi-file comparison
* Financial summarization
* Cloud-based vector storage
* User authentication
* Exportable insights & reports
