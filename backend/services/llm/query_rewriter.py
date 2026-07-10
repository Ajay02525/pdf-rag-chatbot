from services.observability.decorators import measure_latency


class QueryRewriter:
    PRONOUNS = [
        "he",
        "she",
        "his",
        "her",
        "they",
        "them",
        "it",
        "that company",
        "that project",
        "those skills",
    ]

    @staticmethod
    @measure_latency("query-rewriter")
    def should_rewrite(question):

        question = question.lower()

        return any(p in question for p in QueryRewriter.PRONOUNS)

    def rewrite(provider, history, question):

        prompt = f"""
        Conversation:

        {history}

        Rewrite the question into
        a standalone question.

        Question:
        {question}

        Standalone Question:
        """
        return provider.generate(prompt)
