from sentence_transformers import CrossEncoder

from models.retrieval.ranked_document import RankedDocument
from services.observability.decorators import measure_latency


class RerankerService:
    model = CrossEncoder("BAAI/bge-reranker-base")

    @staticmethod
    @measure_latency("reranker")
    def rerank(question, docs, top_k=3):

        pairs = [[question, doc.page_content] for doc in docs]

        scores = RerankerService.model.predict(pairs)

        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        print("\n=== RERANK RESULTS ===")

        ranked_documents = []

        for doc, score in ranked:
            print(f"Score={score:.4f}")
            print(doc.metadata.get("source"))
            print("-" * 50)

            ranked_documents.append(
                RankedDocument(
                    document=doc,
                    score=float(score),
                )
            )

        return ranked_documents[:top_k]
