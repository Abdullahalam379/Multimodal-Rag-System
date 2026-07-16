from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    """
    Central configuration for the application.
    Values are loaded from the .env file or environment variables.
    """

    # -------------------------
    # API Keys
    # -------------------------
    openai_api_key: str

    # -------------------------
    # OpenAI Models
    # -------------------------
    llm_model: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"
    tesseract_cmd: str = os.getenv("TESSERACT_CMD", "tesseract")

    # -------------------------
    # RAG Configuration
    # -------------------------
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 5
    embedding_batch_size: int = 80

    # -------------------------
    # Project Paths
    # -------------------------
    upload_dir: str = "data/uploads"
    images_dir: str = "data/extracted_images"
    vector_db_dir: str = "data/chroma_db"
    collection_name: str = "multimodal_rag"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()