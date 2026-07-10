from contextlib import asynccontextmanager
from fastapi import FastAPI

from services.llm.llm_factory import LLMFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup/shutdown lifecycle.

    Runs once when FastAPI starts.
    """

    print("\n===================================")
    print("Starting PDF RAG Backend...")
    print("===================================")

    # ----------------------------
    # Load Embedding Model
    # ----------------------------
    # EmbeddingService.get_model()
    # its not required for now as we are using Jina Embeddings which is an external service and does not require loading a model in the backend.

    # ----------------------------
    # Initialize LLM Provider
    # ----------------------------
    LLMFactory.get_provider()

    # ----------------------------
    # Load CrossEncoder
    # ----------------------------
    # _ = RerankerService.model

    print("\n===================================")
    print("Application Ready 🚀")
    print("===================================\n")

    yield

    print("\n===================================")
    print("Shutting down application...")
    print("===================================")
