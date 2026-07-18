import requests
import streamlit  as st
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
st.subheader("Document Source")

source = st.radio(
    "Choose how to provide a document",
    [
        "Upload my own PDF",
        "Use a sample PDF",
    ],
)
uploaded_file = None
selected_sample = None

if source == "Upload my own PDF":

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
    )

else:

    sample_map = {
        "Annual Report": "annual_report_sample.pdf",
        "Invoice": "invoice_sample.pdf",
        "Scanned Contract": "scanned_contract.pdf",
    }

    sample_name = st.selectbox(
        "Choose a sample document",
        list(sample_map.keys()),
    )

    selected_sample = sample_map[sample_name]

if st.button("Index Document", use_container_width=True):

    try:

        with st.spinner("Indexing document... This may take a while for large PDFs."):

            if source == "Upload my own PDF":

                if uploaded_file is None:
                    st.warning("Please upload a PDF first.")
                    st.stop()

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf",
                    )
                }

                response = requests.post(
                    f"{API_URL}/index",
                    files=files,
                )

            else:

                response = requests.post(
                    f"{API_URL}/index-sample",
                    json={
                        "sample": selected_sample,
                    },
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
                        result = response.json()

                        st.success("Answer")

                        st.write(result["answer"])

                        st.divider()

                        st.subheader("📚 Retrieved Context")

                        for i, chunk in enumerate(result["retrieved_chunks"], start=1):

                            with st.expander(
                                f"Chunk {i} | Page {chunk['page_number']} | {chunk['content_type'].upper()}",
                                expanded=False,
                            ):
                                st.caption(f"Source: {chunk['source']}")
                                st.write(chunk["content"])
                    

                   

                else:
                    st.error(response.text)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to FastAPI server. Is it running?"
                )


