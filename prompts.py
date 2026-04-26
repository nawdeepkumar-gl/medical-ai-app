def build_prompt(patient_context, chat_history, retrieved_docs, user_query):
    return f"""
You are an AI medical assistant helping a doctor.

Patient Details:
{patient_context}

Chat History:
{chat_history}

Relevant Medical Context:
{retrieved_docs}

Doctor Question:
{user_query}

Instructions:
- Provide medically relevant, structured response
- Do NOT hallucinate
- If unsure, say "Need more clinical information"

Answer:
"""