class QueryClassifier:

    COMPARISON_WORDS = [
        "compare",
        "comparison",
        "difference",
        "different",
        "vs",
        "versus",
        "between",
    ]

    @staticmethod
    def is_comparison(question: str) -> bool:
        """
        Returns True if the query compares
        multiple entities/documents.
        """

        question = question.lower()

        return any(
            word in question
            for word in QueryClassifier.COMPARISON_WORDS
        )

    @staticmethod
    def get_source_limit(question: str) -> int:
        """
        Determines how many documents
        should participate in retrieval.
        """

        if QueryClassifier.is_comparison(question):
            return 5

        return 1