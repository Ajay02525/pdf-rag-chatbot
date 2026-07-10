from collections import defaultdict


class HybridRetriever:
    """
    Hybrid Retriever using Reciprocal Rank Fusion (RRF)

    RRF combines rankings from multiple retrieval
    algorithms instead of combining their scores.

    Reference:
    Reciprocal Rank Fusion
    https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
    """

    RRF_K = 60

    @staticmethod
    def merge(vector_docs, bm25_docs):

        document_scores = defaultdict(float)
        document_lookup = {}

        # ----------------------------------------
        # Vector Search Ranking
        # ----------------------------------------

        for rank, doc in enumerate(vector_docs, start=1):
            key = (
                doc.metadata.get("source"),
                doc.metadata.get("page"),
                doc.page_content,
            )

            document_lookup[key] = doc

            document_scores[key] += 1 / (HybridRetriever.RRF_K + rank)

        # ----------------------------------------
        # BM25 Ranking
        # ----------------------------------------

        for rank, doc in enumerate(bm25_docs, start=1):
            key = (
                doc.metadata.get("source"),
                doc.metadata.get("page"),
                doc.page_content,
            )

            document_lookup[key] = doc

            document_scores[key] += 1 / (HybridRetriever.RRF_K + rank)

        # ----------------------------------------
        # Final Ranking
        # ----------------------------------------

        ranked = sorted(
            document_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        print("\n========== RRF RESULTS ==========")

        for key, score in ranked[:10]:
            print(f"{key[0]} | RRF={score:.5f}")

        print("=================================\n")

        return [document_lookup[key] for key, _ in ranked]
