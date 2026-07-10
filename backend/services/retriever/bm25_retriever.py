from rank_bm25 import BM25Okapi


class BM25Retriever:
    @staticmethod
    def search(question, docs, top_k=20):

        if not docs:
            return []

        corpus = [doc.page_content for doc in docs]

        tokenized_corpus = [doc.lower().split() for doc in corpus]

        bm25 = BM25Okapi(tokenized_corpus)

        tokenized_query = question.lower().split()

        scores = bm25.get_scores(tokenized_query)

        ranked_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

        return [doc for doc, score in ranked_docs[:top_k]]
