from contextlib import asynccontextmanager
from fastapi import FastAPI

from services.embedding.embedding_service import EmbeddingService
from services.llm.llm_factory import LLMFactory
from services.reranker.reranker_service import RerankerService
from services.observability.langfuse_service import LangfuseService


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
    EmbeddingService.get_model()

    # ----------------------------
    # Initialize LLM Provider
    # ----------------------------
    LLMFactory.get_provider()

    # ----------------------------
    # Load CrossEncoder
    # ----------------------------
    _ = RerankerService.model

    # ----------------------------
    # Initialize Langfuse
    # ----------------------------
    LangfuseService.get_client()

    print("\n===================================")
    print("Application Ready 🚀")
    print("===================================\n")

    yield

    print("\n===================================")
    print("Shutting down application...")
    print("===================================")
