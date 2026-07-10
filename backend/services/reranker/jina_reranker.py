import httpx

from config.setting import settings
from models.retrieval.ranked_document import RankedDocument


class JinaReranker:
    URL = settings.JINA_RERANKER_CLIENT_URL

    @staticmethod
    def rerank(question: str, docs: list, top_k: int = 5):

        if not docs:
            return []

        headers = {
            "Authorization": f"Bearer {settings.JINA_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.JINA_RERANKER_MODEL,
            "query": question,
            "top_n": top_k,
            "documents": [doc.page_content for doc in docs],
            "return_documents": False,
        }

        response = httpx.post(
            JinaReranker.URL,
            headers=headers,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        body = response.json()

        ranked = []

        for item in body["results"]:
            ranked.append(
                RankedDocument(
                    document=docs[item["index"]],
                    score=item["relevance_score"],
                )
            )

        return ranked
