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
st.sidebar.subheader("⚙️ Settings")

debug_mode = st.sidebar.checkbox("Show RAG Details")
use_rag = st.sidebar.checkbox("Enable RAG", value=True)

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []

st.sidebar.header("Patient Details")

name = st.sidebar.text_input("Name")
age = st.sidebar.number_input("Age", min_value=0, max_value=120)
symptoms = st.sidebar.text_area("Symptoms")

patient_context = f"""
Name: {name}
Age: {age}
Symptoms: {symptoms}
"""

# Adding cache
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
        #st.session_state.vector_store = create_vector_store(text)

        #Using cache
        st.session_state.vector_store = cached_vector_store(text)

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

    # retrieved_docs = ""
    # if "vector_store" in st.session_state:
    #     retrieved_docs = retrieve_docs(
    #         st.session_state.vector_store,
    #         user_query
    #     )

    docs = []
    retrieved_text = ""

    if use_rag and "vector_store" in st.session_state:
        docs = retrieve_docs(
            st.session_state.vector_store,
            user_query
        )
        retrieved_text = "\n".join([doc.page_content for doc in docs])

    prompt = build_prompt(
        patient_context,
        st.session_state.chat_history,
       # retrieved_docs,
        retrieved_text,
        user_query
    )

    # with st.spinner("Thinking..."):
    #     response = client.chat.completions.create(
    #         model="gpt-4o-mini",
    #         messages=[{"role": "user", "content": prompt}]
    #     )

    # answer = response.choices[0].message.content

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

    # Store history
    st.session_state.chat_history.append(
        {"question": user_query, "answer": answer}
    )

    if debug_mode and docs:
        with st.expander("📄 Retrieved Medical Context"):
            for i, doc in enumerate(docs):
                st.write(f"Chunk {i+1}")
                st.write(doc.page_content)
                st.write("---")

# -----------------------------
# Display Chat
# -----------------------------
# for chat in st.session_state.chat_history:
#     st.markdown(f"**👨‍⚕️ Doctor:** {chat['question']}")
#     st.markdown(f"**🤖 Assistant:** {chat['answer']}")
#     st.markdown("---")


for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["question"])

    with st.chat_message("assistant"):
        st.markdown(chat["answer"])