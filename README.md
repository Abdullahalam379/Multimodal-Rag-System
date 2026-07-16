# 📄 Multimodal RAG System

> A production-style Multimodal Retrieval-Augmented Generation (RAG) system built with FastAPI, ChromaDB, OCR, OpenAI, Docker, Prometheus, Grafana, Streamlit, and GitHub Actions.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![CI](https://img.shields.io/badge/GitHub-Actions-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

# 🚀 Overview

This project is an end-to-end **Multimodal Retrieval-Augmented Generation (RAG)** application capable of answering questions from PDF documents containing both text and images.

Unlike a simple chatbot, this system performs an entire document indexing pipeline:

- 📄 PDF Parsing
- 🖼 OCR on Images
- ✂ Intelligent Text Chunking
- 🧠 Vector Embedding Generation
- 🗄 ChromaDB Vector Storage
- 🔍 Semantic Retrieval
- 🤖 OpenAI Response Generation

The project follows production-inspired software engineering practices including Docker, monitoring, metrics, testing, CI pipelines, and modular architecture.

---

# ✨ Features

- Upload PDF documents
- OCR extraction from embedded images
- Automatic document chunking
- Vector embedding generation
- ChromaDB semantic search
- Retrieval-Augmented Generation (RAG)
- FastAPI REST API
- Streamlit frontend
- Dockerized backend
- Dockerized frontend
- Prometheus metrics
- Grafana dashboards
- Unit/API testing with Pytest
- GitHub Actions CI

---

# 🏗 Project Architecture

```
                PDF Upload
                     │
                     ▼
             PDF Processing
                     │
      ┌──────────────┴─────────────┐
      ▼                            ▼
 Text Extraction             OCR Extraction
      │                            │
      └──────────────┬─────────────┘
                     ▼
              Text Chunking
                     ▼
         OpenAI Embeddings
                     ▼
             ChromaDB Storage
                     ▼
            Semantic Retrieval
                     ▼
              OpenAI LLM
                     ▼
               Final Answer
```

---

# 📂 Project Structure

```
Multimodal-Rag-system
│
├── app/
│   ├── api/
│   ├── core/
│   ├── schemas/
│   ├── services/
│   ├── monitoring/
│   ├── main.py
│
├── tests/
│
├── streamlit_app.py
│
├── Dockerfile
├── Dockerfile.streamlit
├── docker-compose.yml
│
├── prometheus.yml
│
├── pyproject.toml
├── uv.lock
│
└── README.md
```

---

# ⚙ Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM | OpenAI GPT |
| Vector DB | ChromaDB |
| OCR | Tesseract OCR |
| PDF Parsing | PyMuPDF + pdfplumber |
| Embeddings | OpenAI Embeddings |
| Monitoring | Prometheus |
| Dashboards | Grafana |
| Testing | Pytest |
| CI | GitHub Actions |
| Containerization | Docker |
| Package Manager | uv |

---

# 📊 Monitoring

The application exposes Prometheus metrics including:

- API request count
- API latency
- OCR latency
- Embedding latency
- Retrieval latency
- LLM latency
- Complete pipeline latency

Metrics endpoint:

```
/metrics
```

These metrics are visualized using Grafana dashboards.

---

# 🧪 Testing

Run all tests

```bash
pytest
```

Current tests include:

- Health endpoint
- Ask endpoint
- Index endpoint

---

# 🐳 Running with Docker

Build containers

```bash
docker compose build
```

Start services

```bash
docker compose up
```

Backend

```
http://localhost:8000
```

Frontend

```
http://localhost:8501
```

Swagger

```
http://localhost:8000/docs
```

Prometheus

```
http://localhost:9090
```

Grafana

```
http://localhost:3000
```

---

# 💻 Local Development

Clone repository

```bash
git clone https://github.com/Abdullahalam379/Multimodal-Rag-system.git
```

Install dependencies

```bash
uv sync
```

Run backend

```bash
uv run uvicorn app.main:app --reload
```

Run frontend

```bash
streamlit run streamlit_app.py
```

---

# 🔄 CI Pipeline

Every push and pull request automatically:

- Installs dependencies
- Runs Pytest
- Verifies project builds successfully

Powered by GitHub Actions.

---



# 🎯 Future Improvements

- Authentication
- User document isolation
- Hybrid Search (BM25 + Dense Retrieval)
- Redis caching
- Kubernetes deployment
- AWS deployment
- Continuous Deployment
- Integration tests
- Load testing
- Multiple LLM providers

---

# 📚 Learning Outcomes

This project demonstrates practical experience with:

- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Semantic Search
- OCR Pipelines
- FastAPI Development
- Docker
- CI/CD
- Monitoring & Observability
- Software Testing
- Production-style Backend Engineering

---

# 👤 Author

**Abdullah Alam**

AI / ML Engineer

GitHub:
https://github.com/Abdullahalam379

LinkedIn:
https://linkedin.com/in/alam-abdullah/


---

# ⭐ If you found this project useful, consider giving it a star!