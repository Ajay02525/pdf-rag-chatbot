from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
)

# ===========================================
# HTTP Metrics
# ===========================================

REQUEST_COUNT = Counter(
    "rag_http_requests_total",
    "Total HTTP requests handled by the API.",
    ["endpoint", "method", "status"],
)

REQUEST_LATENCY = Histogram(
    "rag_http_request_duration_seconds",
    "HTTP request latency.",
    ["endpoint", "method"],
)

# ===========================================
# RAG Pipeline Metrics
# ===========================================

RAG_STEP_LATENCY = Histogram(
    "rag_step_duration_seconds",
    "Latency of every RAG pipeline step.",
    ["step"],
)

RAG_RETRIEVED_DOCS = Gauge(
    "rag_retrieved_documents",
    "Number of retrieved documents.",
    ["stage"],
)

RAG_CONTEXT_LENGTH = Histogram(
    "rag_context_length_chars",
    "Length of context sent to the LLM.",
)

RAG_SELECTED_SOURCES = Gauge(
    "rag_selected_sources",
    "Number of selected sources.",
)

RAG_ERRORS = Counter(
    "rag_errors_total",
    "Number of RAG errors.",
    ["endpoint", "stage"],
)

# ===========================================
# Guardrail Metrics
# ===========================================

GUARDRAIL_REQUESTS = Counter(
    "rag_guardrail_requests_total",
    "Total number of guardrail validations.",
    ["guardrail"],
)

GUARDRAIL_BLOCKED = Counter(
    "rag_guardrail_blocked_total",
    "Number of blocked guardrail requests.",
    ["guardrail"],
)

GUARDRAIL_LATENCY = Histogram(
    "rag_guardrail_latency_seconds",
    "Latency of guardrail validation.",
    ["guardrail"],
)
