class SourceSelector:
    @staticmethod
    def get_top_sources(docs_with_scores, limit=1):

        best_score = {}

        print("\n===== SOURCE CANDIDATES =====")

        for doc, score in docs_with_scores:
            source = doc.metadata.get("source")

            print(f"{source} -> {score:.4f}")

            if source not in best_score:
                best_score[source] = score
            else:
                best_score[source] = min(best_score[source], score)

        print("\n===== BEST SCORE PER SOURCE =====")

        for source, score in best_score.items():
            print(f"{source} -> {score:.4f}")

        ranked = sorted(best_score.items(), key=lambda x: x[1])

        print("\n===== FINAL RANKING =====")

        for source, score in ranked:
            print(f"{source} -> {score:.4f}")

        return [source for source, _ in ranked[:limit]]
