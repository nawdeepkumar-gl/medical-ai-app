# 🏥 AI Medical Assistant (Doctor Copilot)

## 📌 Overview

This project is a **Streamlit-based AI Medical Assistant** that simulates a real-world clinical decision support system.

It enables doctors to:

* Manage patient records
* Track patient history over multiple visits
* Upload medical documents (PDFs)
* Ask clinical questions
* Receive **context-aware, grounded responses** using Retrieval-Augmented Generation (RAG)

---

## 🎯 Why This Project

This project demonstrates how modern GenAI systems can be built to:

* Reduce hallucinations in LLM responses
* Enable document-grounded medical reasoning
* Maintain **stateful patient memory**
* Simulate real-world healthcare AI systems
* Combine **LLMs + Vector Databases + Patient Context**

---

## 🧠 Key Features

### 👨‍⚕️ Patient Management

* Select existing patients from dropdown
* Add new patients dynamically
* Persistent storage using JSON
* Multi-visit tracking

---

### 📜 Patient History

* View past visits in sidebar
* Stores:

  * Symptoms
  * AI-generated notes
* Enables longitudinal tracking

---

### 🧠 AI-Generated Patient Summary

* One-click clinical summary
* Highlights:

  * Symptom progression
  * Key observations
  * Possible conditions

---

### 📂 Document Upload (RAG)

* Upload medical PDFs (e.g., diabetes guidelines)
* Extract and embed content
* Perform semantic search using FAISS

---

### 🔍 Retrieval-Augmented Generation (RAG)

* Retrieves relevant document chunks
* Injects into prompt
* Generates grounded responses

---

### 💬 Conversational Chat

* Chat interface with memory
* Maintains context across queries

---

### ⚙️ Debug Mode

* View retrieved document chunks
* Understand how RAG works internally

---

### 🛡️ Guardrails

* Only medical queries allowed
* Prevents hallucination
* Uses only provided context
* Safe clinical responses

---

## 🏗️ Architecture

```text
Doctor Query
     ↓
Patient Context (History + Current Visit)
     ↓
Document Retrieval (FAISS)
     ↓
Relevant Medical Chunks
     ↓
Prompt Engineering
     ↓
LLM (OpenAI)
     ↓
Grounded Response
```

---

## 🛠️ Tech Stack

* **Frontend/UI**: Streamlit
* **LLM**: OpenAI API
* **RAG Framework**: LangChain
* **Vector Store**: FAISS
* **PDF Parsing**: PyMuPDF
* **Storage**: JSON (patients database)

---

## 📸 Demo

```
/assets/demo.png
```

*(Add screenshots here for better impact)*

---

## 📁 Project Structure

```text
medical-ai-app/
│── app.py
│── prompts.py
│── rag_pipeline.py
│── patients.json
│── requirements.txt
│── Dockerfile
│── .env
│── utils/
│    ├── pdf_loader.py
│    └── patient_db.py
```

---

# ⚙️ Local Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/medical-ai-assistant.git
cd medical-ai-assistant
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv streamlit_venv
```

---

## 3️⃣ Activate Environment

```bash
# Windows
streamlit_venv\Scripts\activate

# Mac/Linux
source streamlit_venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 🧪 How to Use

### 🔹 Existing Patient

1. Select patient from dropdown
2. View history
3. Generate AI summary
4. Ask clinical questions

---

### 🔹 New Patient

1. Select “New Patient”
2. Enter details
3. Ask question
4. System stores new record

---

### 🔹 With Document (RAG)

1. Upload medical PDF
2. Ask questions
3. View retrieved chunks (Debug Mode)

---

## 🔥 Example Use Case

**Patient:** Amit (Age 50)
**Symptoms:** Fatigue, frequent urination

**Query:**

```text
Based on patient history, what is the likely condition?
```

👉 System:

* Uses patient history
* Retrieves document context
* Generates grounded response

---

## 📝 Notes

* Ensure PDFs contain **selectable text** (not scanned images)
* Responses are grounded in retrieved + patient context
* Not a substitute for real medical advice

---

# 🐳 Docker Setup

## 📦 Prerequisites

* Windows 10/11 (64-bit)
* WSL2 enabled
* Docker Desktop installed

---

## ⚙️ Step 1: Install Docker

1. Download Docker Desktop
   https://www.docker.com/products/docker-desktop/

2. Install and launch Docker Desktop

3. Enable **WSL 2 integration**

---

## 🔍 Step 2: Verify Installation

```bash
docker version
```

Ensure both:

```
Client:
Server:
```

---

## 🔐 Step 3: Fix Permission Issue (WSL)

```bash
sudo usermod -aG docker $USER
```

Then restart WSL (PowerShell):

```bash
wsl --shutdown
```

---

## 📁 Step 4: Navigate to Project

```bash
cd /mnt/d/medical-ai-app
```

---

## 🐳 Step 5: Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 📦 Step 6: Build Docker Image

```bash
docker build -t medical-ai-app .
```

---

## ▶️ Step 7: Run Container

```bash
docker run -p 8501:8501 \
-e OPENAI_API_KEY=your_key \
-e OPENAI_BASE_URL=https://api.openai.com/v1 \
medical-ai-app
```

---

## 🌐 Step 8: Access Application

👉 http://localhost:8501

---

## ⚠️ Common Issues & Fixes

### Docker not running

Start Docker Desktop

---

### Cannot connect to Docker daemon

Enable WSL integration in Docker Desktop

---

### Permission denied

```bash
newgrp docker
```

---

### App not loading

* Check logs in terminal
* Verify `app.py` exists
* Ensure dependencies are installed

---

# 🚀 Future Enhancements

* Patient timeline visualization
* PDF report export
* FastAPI backend
* Database integration (PostgreSQL)
* Authentication system
* Multi-user support
* Cloud deployment (AWS / Azure)

---

## 🎓 Learning Outcomes

* Build RAG-based applications
* Design stateful AI systems
* Integrate LLM + UI + data
* Apply GenAI in healthcare

---

## 📄 License

For educational purposes only.
