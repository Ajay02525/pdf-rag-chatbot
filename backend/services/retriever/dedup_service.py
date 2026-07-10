from collections import defaultdict


class DedupService:
    @staticmethod
    def keep_best_chunks(
        docs_with_scores,
        per_page=1,
        per_document=3,
    ):

        # -----------------------------
        # Step 1
        # Best chunk per page
        # -----------------------------

        page_best = {}

        for doc, score in docs_with_scores:
            page_key = (
                doc.metadata.get("source"),
                doc.metadata.get("page"),
            )

            if page_key not in page_best:
                page_best[page_key] = (doc, score)

            elif score < page_best[page_key][1]:
                page_best[page_key] = (doc, score)

        # -----------------------------
        # Step 2
        # Limit chunks per document
        # -----------------------------

        grouped = defaultdict(list)

        for doc, score in page_best.values():
            grouped[doc.metadata.get("source")].append((doc, score))

        final_docs = []

        for source, docs in grouped.items():
            docs.sort(key=lambda x: x[1])

            final_docs.extend(docs[:per_document])

        final_docs.sort(key=lambda x: x[1])

        return final_docs
