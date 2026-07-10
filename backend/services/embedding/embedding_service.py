from langchain_huggingface import HuggingFaceEmbeddings
from config.setting import settings


class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:
            print("Loading Embedding Model...")
            cls._model = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
            print("Embedding Model Ready.")

        return cls._model
