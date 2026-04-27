from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def create_vector_store(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)

    return vector_store


# def retrieve_docs(vector_store, query):
#     docs = vector_store.similarity_search(query, k=3)
#     return "\n".join([doc.page_content for doc in docs])


def retrieve_docs(vector_store, query):
    docs = vector_store.similarity_search(query, k=3)
    return docs   # return full docs, NOT joined text