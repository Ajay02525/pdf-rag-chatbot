from services.embedding.jina_embeddings import JinaEmbeddings


class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:
            cls._model = JinaEmbeddings()

        return cls._model
