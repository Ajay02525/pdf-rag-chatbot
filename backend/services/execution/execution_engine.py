from datetime import datetime
from typing import Any


class ExecutionEngine:
    """
    Generic AI Execution Engine.

    Records every completed execution step of an AI workflow.

    Current Use Cases
    -----------------
    - RAG
    - AI Agents
    - SQL Agent
    - Browser Agent
    - Multi-Agent Workflow

    The frontend simply consumes:

        engine.build()

    to render the AI Execution Visualizer.
    """

    def __init__(
        self,
        session_id: str,
        provider: str,
        model: str,
    ):

        self.pipeline = {
            "header": {
                # Session
                "session_id": session_id,
                # LLM
                "provider": provider,
                "model": model,
                "temperature": None,
                # Retrieval
                "embedding_model": None,
                "vector_database": None,
                # Timing
                "started_at": datetime.utcnow(),
                "completed_at": None,
                "total_duration_ms": None,
                # Token Usage (Future)
                "input_tokens": None,
                "output_tokens": None,
                "total_tokens": None,
                # Cost (Future)
                "cost": None,
            },
            "steps": [],
        }

    # =====================================================
    # Header
    # =====================================================

    def update_header(self, **kwargs):
        """
        Update header metadata.

        Example
        -------
        engine.update_header(
            temperature=0.1,
            embedding_model="BAAI/bge-base-en-v1.5",
            vector_database="ChromaDB"
        )
        """

        self.pipeline["header"].update(kwargs)

    # =====================================================
    # Timer
    # =====================================================

    def start_timer(self):
        """
        Start timer for an execution step.
        """

        return datetime.utcnow()

    # =====================================================
    # Record Step
    # =====================================================

    def record(
        self,
        start_time: datetime,
        id: str,
        title: str,
        icon: str,
        fields: dict[str, Any] | None = None,
        status: str = "completed",
        children: list | None = None,
    ):
        """
        Record a completed execution step.
        """

        duration = (datetime.utcnow() - start_time).total_seconds() * 1000

        self.pipeline["steps"].append(
            {
                "id": id,
                "title": title,
                "icon": icon,
                "status": status,
                "duration_ms": round(duration, 2),
                "fields": fields or {},
                "children": children or [],
            }
        )

    # =====================================================
    # Build Final Pipeline
    # =====================================================

    def build(self):
        """
        Build the final execution pipeline.
        """

        completed = datetime.utcnow()

        self.pipeline["header"]["completed_at"] = completed

        total_duration = (
            completed - self.pipeline["header"]["started_at"]
        ).total_seconds() * 1000

        self.pipeline["header"]["total_duration_ms"] = round(
            total_duration,
            2,
        )

        # Convert datetime objects to ISO strings

        self.pipeline["header"]["started_at"] = self.pipeline["header"][
            "started_at"
        ].isoformat()

        self.pipeline["header"]["completed_at"] = self.pipeline["header"][
            "completed_at"
        ].isoformat()

        return self.pipeline
