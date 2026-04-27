# 🏥 AI Medical Assistant (Doctor Copilot)

## 📌 Overview

This project is a **Streamlit-based AI Medical Assistant** that simulates a real-world clinical decision support system.

It enables doctors to:

* Manage patient records
* Track patient history over multiple visits
* Upload medical documents (PDFs)
* Ask clinical questions
* Receive **context-aware, grounded responses** using RAG (Retrieval-Augmented Generation)

---

## 🎯 Objective

To demonstrate how modern GenAI systems combine:

* 🧠 Large Language Models (LLMs)
* 📂 Retrieval-Augmented Generation (RAG)
* 🧾 Patient memory (stateful systems)
* 💬 Conversational interfaces

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

### 🔍 Retrieval-Augmented Generation

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

## 📁 Project Structure

```text
medical-ai-app/
│── app.py
│── prompts.py
│── rag_pipeline.py
│── patients.json
│── requirements.txt
│── .env
│── utils/
│    ├── pdf_loader.py
│    └── patient_db.py
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/<your-username>/medical-ai-assistant.git
cd medical-ai-assistant
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv streamlit_venv
```

---

### 3️⃣ Activate Environment

```bash
# Windows
streamlit_venv\Scripts\activate

# Mac/Linux
source streamlit_venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create `.env` file:

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

## 🎓 Learning Outcomes

* Understand RAG systems
* Build stateful AI applications
* Integrate LLM + UI + data
* Design safe AI systems for healthcare

---

## 🚀 Future Enhancements

* Patient dashboard with filters
* Timeline visualization
* FastAPI backend
* Database integration
* Authentication system

---

## 📄 License

For educational purposes only.
