import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

from utils.pdf_loader import load_pdf
from rag_pipeline import create_vector_store, retrieve_docs
from prompts import build_prompt

# Patient DB
from utils.patient_db import add_or_update_patient, get_patient_summary

# Get all patients' name and patient's full history
from utils.patient_db import get_all_patients, get_patient_full_history

# -----------------------------
# Load environment
# -----------------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

def generate_patient_summary(history):

    if not history:
        return "No history available."

    history_text = ""
    for visit in history:
        history_text += f"Date: {visit['date']}, Symptoms: {visit['symptoms']}\n"

    prompt = f"""
You are a medical assistant.

Summarize the patient's history in a concise clinical format.

History:
{history_text}

Provide a short summary with:
- Key conditions
- Symptom progression
- Important observations
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Medical AI Assistant", layout="wide")
st.title("🏥 AI Medical Assistant (Doctor Copilot)")

st.subheader("📊 Patient Dashboard")

patients = get_all_patients()

if patients:
    for p in patients:
        st.markdown(f"👤 {p}")
else:
    st.info("No patients available yet.")

# -----------------------------
# Sidebar Settings
# -----------------------------
st.sidebar.subheader("⚙️ Settings")

debug_mode = st.sidebar.checkbox("Show RAG Details")
use_rag = st.sidebar.checkbox("Enable RAG", value=True)

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []

# -----------------------------
# Patient Input
# -----------------------------
st.sidebar.header("Patient Details")



patients_list = get_all_patients()

selected_patient = st.sidebar.selectbox(
    "Select Patient",
    ["New Patient"] + patients_list
)

if selected_patient == "New Patient":
    name = st.sidebar.text_input("Enter New Patient Name")
else:
    name = selected_patient

#name = st.sidebar.text_input("Name")


age = st.sidebar.number_input("Age", min_value=0, max_value=120)
symptoms = st.sidebar.text_area("Symptoms")

# -----------------------------
# Patient History
# -----------------------------
patient_history = get_patient_summary(name)

st.sidebar.subheader("📜 Patient History")
st.sidebar.write(patient_history)

# AI Summary
if name:
    full_history = get_patient_full_history(name)

    if full_history:
        if st.sidebar.button("🧠 Generate Patient Summary"):
            summary = generate_patient_summary(full_history)
            st.sidebar.subheader("🧾 AI Summary")
            st.sidebar.write(summary)

# -----------------------------
# Cache Vector Store
# -----------------------------
@st.cache_resource
def cached_vector_store(text):
    return create_vector_store(text)

# -----------------------------
# PDF Upload
# -----------------------------
st.subheader("📂 Upload Medical Document")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    with st.spinner("Processing PDF..."):
        text = load_pdf(uploaded_file)
        st.session_state.vector_store = cached_vector_store(text)
        st.success("Document processed!")

# -----------------------------
# Chat State
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Chat Interface
# -----------------------------
st.subheader("💬 Ask the Assistant")

user_query = st.text_input("Enter your question")

if st.button("Ask AI"):

    if not name:
        st.warning("Please enter patient name")
        st.stop()

    if not user_query:
        st.warning("Please enter a question")
        st.stop()

    # -----------------------------
    # Show user message
    # -----------------------------
    with st.chat_message("user"):
        st.markdown(user_query)

    # -----------------------------
    # Convert chat history → text
    # -----------------------------
    chat_history_text = ""
    for chat in st.session_state.chat_history:
        chat_history_text += f"Doctor: {chat['question']}\nAssistant: {chat['answer']}\n"

    # -----------------------------
    # Build full patient context
    # -----------------------------
    full_patient_context = f"""
Current Visit:
Name: {name}
Age: {age}
Symptoms: {symptoms}

Previous History:
{patient_history}
"""

    # -----------------------------
    # Retrieval (RAG)
    # -----------------------------
    docs = []
    retrieved_text = ""

    if use_rag and "vector_store" in st.session_state:
        docs = retrieve_docs(
            st.session_state.vector_store,
            user_query
        )
        retrieved_text = "\n".join([doc.page_content for doc in docs])

    # -----------------------------
    # Build Prompt
    # -----------------------------
    prompt = build_prompt(
        full_patient_context,
        chat_history_text,
        retrieved_text,
        user_query
    )

    # -----------------------------
    # LLM Streaming Response
    # -----------------------------
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full_response += delta
            placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    answer = full_response

    # -----------------------------
    # Save Chat History
    # -----------------------------
    st.session_state.chat_history.append(
        {"question": user_query, "answer": answer}
    )

    # -----------------------------
    # Save Patient Visit
    # -----------------------------
    if name and symptoms:
        add_or_update_patient(name, symptoms, answer)

    # -----------------------------
    # Debug: Show Retrieved Docs
    # -----------------------------
    if debug_mode and docs:
        with st.expander("📄 Retrieved Medical Context"):
            for i, doc in enumerate(docs):
                st.write(f"Chunk {i+1}")
                st.write(doc.page_content)
                st.write("---")

# -----------------------------
# Display Chat History
# -----------------------------
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["question"])

    with st.chat_message("assistant"):
        st.markdown(chat["answer"])