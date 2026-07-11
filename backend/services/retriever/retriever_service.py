from services.embedding.embedding_service import EmbeddingService
from services.retriever.vector_retriever import VectorRetriever
from services.retriever.query_classifier import QueryClassifier
from services.retriever.source_selector import SourceSelector
from services.retriever.bm25_retriever import BM25Retriever
from services.retriever.hybrid_retriever import HybridRetriever

from services.reranker.reranker_service import RerankerService
from services.retriever.dedup_service import DedupService
from models.retrieval.retrieval_result import RetrievalResult
from config.setting import settings


class RetrieverService:
    @staticmethod
    def retrieve(question: str):
        execution = []
        embedding = EmbeddingService.get_model()
        execution.append(
            {
                "id": "embedding",
                "title": "Query Embedding",
                "icon": "cpu",
                "status": "completed",
                "fields": {
                    "Embedding Model": settings.EMBEDDING_MODEL,
                    "Dimension": settings.JINA_EMBEDDING_DIMENSIONS,
                },
            }
        )
        # -----------------------------------------
        # Initial Dense Retrieval
        # -----------------------------------------

        docs_with_scores = VectorRetriever.search_with_score(
            question,
            embedding,
            k=50,
        )
        execution.append(
            {
                "id": "vector_search",
                "title": "Vector Search",
                "icon": "database",
                "status": "completed",
                "fields": {
                    "Initial Candidates": len(docs_with_scores),
                    "Search K": 50,
                },
            }
        )

        is_comparison = QueryClassifier.is_comparison(question)

        # =========================================
        # NORMAL QUERY
        # =========================================

        if not is_comparison:
            print("\n=== NORMAL RETRIEVAL ===")

            # Keep only the best chunk from each page
            docs_with_scores = DedupService.keep_best_chunks(docs_with_scores)
            execution.append(
                {
                    "id": "dedup",
                    "title": "Deduplication",
                    "icon": "copy-x",
                    "status": "completed",
                    "fields": {
                        "Remaining Chunks": len(docs_with_scores),
                    },
                }
            )
            vector_docs = [doc for doc, _ in docs_with_scores]

        # =========================================
        # COMPARISON QUERY
        # =========================================

        else:
            print("\n=== COMPARISON RETRIEVAL ===")

            source_limit = QueryClassifier.get_source_limit(question)

            sources = SourceSelector.get_top_sources(
                docs_with_scores,
                limit=source_limit,
            )

            print("Sources :", sources)

            vector_docs = []

            for source in sources:
                docs = VectorRetriever.search(
                    question,
                    embedding,
                    source=source,
                    k=10,
                )

                # Convert to (doc, dummy_score)
                docs = [(doc, 0) for doc in docs]

                docs = DedupService.keep_best_chunks(docs, per_document=10)

                vector_docs.extend(doc for doc, _ in docs)
        # -----------------------------------------
        # BM25
        # -----------------------------------------

        bm25_docs = BM25Retriever.search(
            question,
            vector_docs,
            top_k=20,
        )
        execution.append(
            {
                "id": "bm25",
                "title": "BM25 Retrieval",
                "icon": "search",
                "status": "completed",
                "fields": {
                    "BM25 Results": len(bm25_docs),
                },
            }
        )
        # -----------------------------------------
        # Hybrid Merge
        # -----------------------------------------

        all_docs = HybridRetriever.merge(
            vector_docs,
            bm25_docs,
        )
        execution.append(
            {
                "id": "hybrid",
                "title": "Hybrid Merge",
                "icon": "git-merge",
                "status": "completed",
                "fields": {
                    "Merged Results": len(all_docs),
                },
            }
        )
        # -----------------------------------------
        # Reranker
        # -----------------------------------------

        top_k = 8 if is_comparison else 5

        ranked_docs = RerankerService.rerank(
            question,
            all_docs,
            top_k=top_k,
        )

        # For now, we are not using reranker as it is not working well with comparison queries. We will use it later when we have a better reranker model.
        scores = [doc.score for doc in ranked_docs]
        execution.append(
            {
                "id": "reranker",
                "title": "Jina Reranker",
                "model": settings.JINA_RERANKER_MODEL,
                "icon": "arrow-up-down",
                "status": "completed",
                "fields": {
                    "model": settings.JINA_RERANKER_MODEL,
                    "Top K": top_k,
                    "Returned": len(ranked_docs),
                    "Highest Score": max(scores) if scores else 0,
                },
            }
        )

        return RetrievalResult(
            documents=ranked_docs,
            retrieved_chunks=len(ranked_docs),
            highest_score=max(scores) if scores else 0.0,
            average_score=sum(scores) / len(scores) if scores else 0.0,
            execution=execution,
        )
