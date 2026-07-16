import requests
import streamlit as st
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Multimodal RAG System",
    page_icon="📄",
    layout="centered",
)

st.title("📄 Multimodal RAG System")
st.write(
    "Upload a PDF, index it into the knowledge base, and ask questions about it."
)

st.divider()

# -----------------------------
# Upload Section
# -----------------------------
st.subheader("Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type=["pdf"],
)

if st.button("Index Document", use_container_width=True):

    if uploaded_file is None:
        st.warning("Please upload a PDF first.")

    else:
        with st.spinner("Indexing document... This may take a while for large PDFs."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf",
                )
            }

            try:
                response = requests.post(
                    f"{API_URL}/index",
                    files=files,
                )

                if response.status_code == 200:
                    summary = response.json()

                    st.success("Document indexed successfully!")

                    st.json(summary)

                else:
                    st.error(response.text)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to FastAPI server. Is it running?"
                )

st.divider()

# -----------------------------
# Question Section
# -----------------------------
st.subheader("Ask a Question")

question = st.text_input(
    "Enter your question",
)

if st.button("Ask", use_container_width=True):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Generating answer..."):

            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question,
                    },
                )

                if response.status_code == 200:

                    answer = response.json()["answer"]

                    st.success("Answer")

                    st.write(answer)

                else:
                    st.error(response.text)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to FastAPI server. Is it running?"
                )
                