import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

from utils.pdf_loader import load_pdf
from rag_pipeline import create_vector_store, retrieve_docs
from prompts import build_prompt

# Load env
load_dotenv()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")  
)

st.set_page_config(page_title="Medical AI Assistant", layout="wide")

st.title("🏥 AI Medical Assistant (Doctor Copilot)")

# -----------------------------
# Sidebar: Patient Context
# -----------------------------
st.sidebar.header("Patient Details")

name = st.sidebar.text_input("Name")
age = st.sidebar.number_input("Age", min_value=0, max_value=120)
symptoms = st.sidebar.text_area("Symptoms")

patient_context = f"""
Name: {name}
Age: {age}
Symptoms: {symptoms}
"""

# -----------------------------
# PDF Upload
# -----------------------------
st.subheader("📂 Upload Medical Document")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    with st.spinner("Processing PDF..."):
        text = load_pdf(uploaded_file)
        st.session_state.vector_store = create_vector_store(text)
        st.success("Document processed!")

# -----------------------------
# Session State for Chat
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Chat Interface
# -----------------------------
st.subheader("💬 Ask the Assistant")

user_query = st.text_input("Enter your question")

if st.button("Ask AI"):

    if not user_query:
        st.warning("Please enter a question")
        st.stop()

    retrieved_docs = ""
    if "vector_store" in st.session_state:
        retrieved_docs = retrieve_docs(
            st.session_state.vector_store,
            user_query
        )

    prompt = build_prompt(
        patient_context,
        st.session_state.chat_history,
        retrieved_docs,
        user_query
    )

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

    answer = response.choices[0].message.content

    # Store history
    st.session_state.chat_history.append(
        {"question": user_query, "answer": answer}
    )

# -----------------------------
# Display Chat
# -----------------------------
for chat in st.session_state.chat_history:
    st.markdown(f"**👨‍⚕️ Doctor:** {chat['question']}")
    st.markdown(f"**🤖 Assistant:** {chat['answer']}")
    st.markdown("---")