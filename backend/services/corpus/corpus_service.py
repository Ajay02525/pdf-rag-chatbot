from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


class CorpusService:
    @staticmethod
    def get_all_documents(embedding):
        db = Chroma(
            persist_directory="data/chroma_db",
            embedding_function=embedding,
        )

        data = db.get()

        docs = []

        for text, metadata in zip(data["documents"], data["metadatas"]):
            docs.append(
                Document(
                    page_content=text,
                    metadata=metadata,
                )
            )

        return docs
