from langchain_chroma import Chroma
from config.setting import settings


class VectorStore:
    @staticmethod
    def create(chunk, embedding):

        db = Chroma.from_documents(
            documents=chunk,
            embedding=embedding,
            persist_directory=settings.CHROMA_DIR,
        )

        print("=" * 80)
        print("TOTAL CHUNKS IN CHROMA:", db._collection.count())
        return db
