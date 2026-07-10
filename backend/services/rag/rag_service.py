import asyncio
import os

from services.memory.chat_memory import ChatMemory

from services.llm.llm_factory import LLMFactory
from services.llm.query_rewriter import QueryRewriter

from services.retriever.retriever_service import RetrieverService
from services.retriever.query_classifier import QueryClassifier

from services.rag.context_builder import ContextBuilder
from services.rag.prompt_builder import PromptBuilder
from services.rag.response_builder import ResponseBuilder
from services.observability.langfuse_service import LangfuseService


from services.guardrails.guardrail_service import GuardrailService
from services.guardrails.output.output_pii import OutputPIIGuardrail
from services.guardrails.output.hallucination import HallucinationGuardrail

from services.guardrails.retrieval.context_validator import (
    ContextValidator,
)

from services.execution.execution_engine import ExecutionEngine
# from services.evaluator.evaluator_service import EvaluatorService


class RAGService:
    """
    Main RAG Orchestrator.

    Responsibilities
    ----------------
    1. Manage Chat History
    2. Rewrite Follow-up Questions
    3. Retrieve Relevant Documents
    4. Build Context
    5. Build Prompt
    6. Generate Response
    7. Save Conversation
    8. Return API Response

    NOTE:
    This class should NEVER contain retrieval,
    reranking or prompt engineering logic.
    """

    provider = LLMFactory.get_provider()

    @staticmethod
    async def ask(question: str, session_id: str):

        ### create an execution engine to track the steps of the RAG process
        engine = ExecutionEngine(
            session_id=session_id,
            provider="Groq",
            model=RAGService.provider.model,
        )
        engine.update_header(
            temperature=0.1,
            embedding_model="BAAI/bge-base-en-v1.5",
            vector_database="ChromaDB",
        )
        start = engine.start_timer()

        engine.record(
            start_time=start,
            id="query",
            title="User Query",
            icon="message",
            fields={
                "Question": question,
                "Characters": len(question),
                "Words": len(question.split()),
                "session_id": session_id,
            },
        )
        ###----------------------------------------------------------------------
        ### Guardrails for user input
        start = engine.start_timer()
        result = GuardrailService.validate(question)
        engine.record(
            start_time=start,
            id="guardrails",
            title="Input Guardrails",
            icon="shield-check",
            fields={
                "Allowed": result.allowed,
                "Reason": result.reason,
            },
        )
        if not result.allowed:
            yield {
                "type": "delta",
                "delta": result.reason,
            }
            yield {
                "type": "sources",
                "sources": [],
            }
            yield {
                "type": "pipeline",
                "pipeline": engine.build(),
            }
            return

        langfuse = LangfuseService.get_client()
        with langfuse.start_as_current_observation(name="pdf-rag-chat"):
            langfuse.update_current_span(
                input=question,
                metadata={
                    "session_id": session_id,
                },
            )
            print("\n==============================")
            print("Original Question:")
            print(question)
            print("==============================")

            # -------------------------------------------------
            # Step 1 : Load Conversation History
            # -------------------------------------------------
            start = engine.start_timer()
            history = ChatMemory.format_history(session_id)
            engine.record(
                start_time=start,
                id="memory",
                title="Chat Memory",
                icon="messages-square",
                fields={
                    "Session": session_id,
                    "History Messages": len(history),
                },
            )
            ChatMemory.add_message(
                session_id,
                "user",
                question,
            )

            # -------------------------------------------------
            # Step 2 : Rewrite Follow-up Question
            # -------------------------------------------------
            with langfuse.start_as_current_observation(name="query-rewrite"):
                start = engine.start_timer()
                if QueryRewriter.should_rewrite(question):
                    standalone_question = QueryRewriter.rewrite(
                        RAGService.provider,
                        history,
                        question,
                    )

                else:
                    standalone_question = question
                langfuse.update_current_span(
                    input=question,
                    output=standalone_question,
                )
                engine.record(
                    start_time=start,
                    id="query_rewriter",
                    title="Query Rewriter",
                    icon="git-branch",
                    fields={
                        "Original Question": question,
                        "Standalone Question": standalone_question,
                        "Rewritten": question != standalone_question,
                    },
                )

            print("\nStandalone Question:")
            print(standalone_question)

            # -------------------------------------------------
            # Step 3 : Retrieve Documents
            # -------------------------------------------------
            with langfuse.start_as_current_observation(name="retrieval"):
                start = engine.start_timer()
                retrieval = RetrieverService.retrieve(standalone_question)
                docs = [ranked.document for ranked in retrieval.documents]
                engine.record(
                    start_time=start,
                    id="retriever",
                    title="Retriever",
                    icon="database",
                    fields={
                        "Search Type": "Hybrid Search",
                        "Embedding Model": "BAAI/bge-base-en-v1.5",
                        "Vector DB": "ChromaDB",
                        "Chunks Retrieved": len(docs),
                        "Highest Score": retrieval.highest_score,
                        "Average Score": retrieval.average_score,
                        "Retrieved Documents": [
                            {
                                "file": ranked.document.metadata.get("source"),
                                "page": ranked.document.metadata.get("page"),
                                "score": ranked.score,
                            }
                            for ranked in retrieval.documents
                        ],
                    },
                    children=retrieval.execution,
                )
                start = engine.start_timer()
                validator = ContextValidator()
                ContextValidatorResult = validator.validate(docs)
                engine.record(
                    start_time=start,
                    id="context_validator",
                    title="Context Validator",
                    icon="badge-check",
                    fields={
                        "Status": "Passed"
                        if ContextValidatorResult.allowed
                        else "Failed",
                        "Reason": ContextValidatorResult.reason,
                    },
                )
                if not ContextValidatorResult.allowed:
                    yield {
                        "type": "delta",
                        "delta": ContextValidatorResult.reason,
                    }

                    yield {
                        "type": "sources",
                        "sources": [],
                    }

                    return

                langfuse.update_current_span(
                    metadata={
                        "chunks": len(docs),
                        "validation": ContextValidatorResult.allowed,
                        "reason": ContextValidatorResult.reason,
                        "highest_score": retrieval.highest_score,
                        "average_score": retrieval.average_score,
                        "sources": [
                            ranked.document.metadata.get("source")
                            for ranked in retrieval.documents
                        ],
                    }
                )

            print(f"\nRetrieved Documents : {len(docs)}")

            # -------------------------------------------------
            # Step 4 : Build Context
            # -------------------------------------------------
            with langfuse.start_as_current_observation(name="context-builder"):
                start = engine.start_timer()
                context = ContextBuilder.build(docs)
                engine.record(
                    start_time=start,
                    id="context_builder",
                    title="Context Builder",
                    icon="file-stack",
                    fields={
                        "Context Characters": len(context),
                        "Words": len(context.split()),
                        "Chunks": len(docs),
                    },
                )
                langfuse.update_current_span(metadata={"context_length": len(context)})
            print(f"Context Length : {len(context)}")

            # -------------------------------------------------
            # Step 5 : Prompt Builder
            # -------------------------------------------------
            with langfuse.start_as_current_observation(name="prompt-builder"):
                start = engine.start_timer()
                prompt = PromptBuilder.build(
                    question=question,
                    context=context,
                    comparison=QueryClassifier.is_comparison(standalone_question),
                )
                engine.record(
                    start_time=start,
                    id="prompt_builder",
                    title="Prompt Builder",
                    icon="file-code",
                    fields={
                        "Prompt Length": len(prompt),
                        "Prompt Characters": len(prompt),
                        "Prompt Words": len(prompt.split()),
                        "Comparison Query": QueryClassifier.is_comparison(
                            standalone_question
                        ),
                    },
                )

            # -------------------------------------------------
            # Step 6 : Generate Answer
            # -------------------------------------------------
            with langfuse.start_as_current_observation(name="llm-generation"):
                start = engine.start_timer()
                full_answer = ""
                for token in RAGService.provider.stream(prompt):
                    full_answer += token
                    yield {
                        "type": "delta",
                        "delta": token,
                    }
                await asyncio.sleep(0.02)

                engine.record(
                    start_time=start,
                    id="llm_generation",
                    title="LLM Generation",
                    icon="brain-circuit",
                    fields={
                        "Provider": "Groq",
                        "Model": RAGService.provider.model,
                        "Temperature": 0.1,
                        "Streaming": True,
                    },
                )

                # Ensure all tokens are sent before proceeding

                # -------------------------------------------------
                # Step 6.1 : Adding Evaluator for llm output
                # -------------------------------------------------
                # evaluation = EvaluatorService.evaluate(
                #     question=question,
                #     answer=answer,
                #     docs=docs,
                # )

                # if not evaluation.allowed:
                #     answer = evaluation.reason
                # -------------------------------------------------
                # Step 7 : Guardrails for llm output
                # -------------------------------------------------
                full_answer = OutputPIIGuardrail.sanitize(full_answer)
                start = engine.start_timer()
                hallucination = HallucinationGuardrail.validate(
                    full_answer,
                    docs,
                )
                engine.record(
                    start_time=start,
                    id="output_guardrails",
                    title="Output Guardrails",
                    icon="shield-alert",
                    fields={
                        "PII Sanitized": "Yes",
                        "Hallucination": "Passed"
                        if hallucination.allowed
                        else "Failed",
                    },
                )
                if not hallucination.allowed:
                    full_answer = hallucination.reason

                langfuse.update_current_generation(
                    input=prompt, output=full_answer, model=os.getenv("GROQ_MODEL")
                )
            # -------------------------------------------------
            # Step 8 : Save Assistant Response
            # -------------------------------------------------

            ChatMemory.add_message(
                session_id,
                "assistant",
                full_answer,
            )

            # -------------------------------------------------
            # Step 9 : Build Final Response
            # -------------------------------------------------
            langfuse.update_current_span(output=full_answer)
            langfuse.flush()
            start = engine.start_timer()
            response_builder = ResponseBuilder.build(
                answer=full_answer,
                docs=docs,
            )
            engine.record(
                start_time=start,
                id="response_builder",
                title="Response Builder",
                icon="sparkles",
                fields={
                    "Answer Characters": len(full_answer),
                    "Sources Returned": len(response_builder["Source"]),
                },
            )
            yield {
                "type": "sources",
                "sources": response_builder["Source"],
            }
            yield {
                "type": "pipeline",
                "pipeline": engine.build(),
            }
