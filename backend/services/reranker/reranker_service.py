from services.observability.decorators import measure_latency
from services.reranker.jina_reranker import JinaReranker


class RerankerService:
    @staticmethod
    @measure_latency("reranker")
    def rerank(question, docs, top_k=5):

        print("\n=== JINA RERANKER ===")

        return JinaReranker.rerank(
            question=question,
            docs=docs,
            top_k=top_k,
        )
