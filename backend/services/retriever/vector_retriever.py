from langchain_community.vectorstores import Chroma


class VectorRetriever:
    @staticmethod
    def search(question, embedding, source=None, k=20):

        db = Chroma(persist_directory="data/chroma_db", embedding_function=embedding)

        if source:
            return db.similarity_search(question, k=k, filter={"source": source})

        return db.similarity_search(question, k=k)

    @staticmethod
    def search_with_score(question, embedding, k=40):

        db = Chroma(persist_directory="data/chroma_db", embedding_function=embedding)

        return db.similarity_search_with_score(question, k=k)
