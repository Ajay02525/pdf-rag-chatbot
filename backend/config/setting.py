from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "PDF RAG Chatbot"
    APP_ENV: str = "development"
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:3000"
    # API
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    UPLOAD_DIR: str = "data/uploads"

    # LLM
    LLM_PROVIDER: str = "groq"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_TEMPERATURE: float = 0.1
    GROQ_API_KEY: str

    # Embedding
    EMBEDDING_MODEL: str = "BAAI/bge-base-en-v1.5"
    EMBEDDING_PROVIDER: str = "jina"
    JINA_API_KEY: str
    JINA_EMBEDDING_MODEL: str = "jina-embeddings-v5-text-small"
    JINA_CLIENT_URL: str = "https://api.jina.ai/v1/embeddings"
    JINA_EMBEDDING_DIMENSIONS: int = 768

    # Vector DB
    CHROMA_DIR: str = "data/chroma_db"

    # Retrieval
    JINA_RERANKER_MODEL: str = "jina-reranker-v3"
    JINA_RERANKER_CLIENT_URL: str = "https://api.jina.ai/v1/rerank"
    SEARCH_K: int = 50
    TOP_K: int = 5

    # Langfuse
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
