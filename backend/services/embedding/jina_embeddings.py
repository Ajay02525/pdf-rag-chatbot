from langchain_core.embeddings import Embeddings
from services.embedding.jina_client import JinaClient


class JinaEmbeddings(Embeddings):
    def embed_documents(self, texts):

        return JinaClient.embed_sync(
            texts,
            task="retrieval.passage",
        )

    def embed_query(self, text):

        return JinaClient.embed_sync(
            [text],
            task="retrieval.query",
        )[0]
