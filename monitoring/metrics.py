from prometheus_client import Counter, Histogram

# -------------------------
# API Metrics
# -------------------------

REQUEST_COUNT = Counter(
    "request_count_total",
    "Total number of API requests",
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "API request latency",
)

# -------------------------
# OCR
# -------------------------

OCR_TIME = Histogram(
    "ocr_processing_seconds",
    "OCR processing time",
)

# -------------------------
# Embedding
# -------------------------

EMBEDDING_TIME = Histogram(
    "embedding_seconds",
    "Embedding generation time",
)

# -------------------------
# Retrieval
# -------------------------

RETRIEVAL_TIME = Histogram(
    "retrieval_seconds",
    "Vector retrieval time",
)

# -------------------------
# LLM
# -------------------------

LLM_RESPONSE_TIME = Histogram(
    "llm_response_seconds",
    "LLM response time",
)

# -------------------------
# Entire Pipeline
# -------------------------

TOTAL_PIPELINE_TIME = Histogram(
    "pipeline_seconds",
    "Complete indexing pipeline",
)