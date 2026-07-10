import httpx

from config.setting import settings


class JinaClient:
    URL = settings.JINA_CLIENT_URL

    @staticmethod
    async def embed(texts: list[str], task: str = "retrieval.passage"):

        headers = {
            "Authorization": f"Bearer {settings.JINA_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.JINA_EMBEDDING_MODEL,
            "task": task,
            "dimensions": settings.JINA_EMBEDDING_DIMENSIONS,
            "normalized": True,
            "input": texts,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                JinaClient.URL,
                headers=headers,
                json=payload,
            )

        response.raise_for_status()

        body = response.json()

        return [item["embedding"] for item in body["data"]]

    @staticmethod
    def embed_sync(
        texts: list[str],
        task="retrieval.passage",
    ):

        headers = {
            "Authorization": f"Bearer {settings.JINA_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.JINA_EMBEDDING_MODEL,
            "task": task,
            "dimensions": settings.JINA_EMBEDDING_DIMENSIONS,
            "normalized": True,
            "input": texts,
        }

        response = httpx.post(
            JinaClient.URL,
            headers=headers,
            json=payload,
            timeout=60,
        )

        response.raise_for_status()
        print("=" * 80)
        print("JINA PAYLOAD")
        print(payload)
        print("=" * 80)
        body = response.json()
        print("=" * 80)
        print("Embedding dimension:", len(body["data"][0]["embedding"]))
        print("=" * 80)

        return [item["embedding"] for item in body["data"]]
