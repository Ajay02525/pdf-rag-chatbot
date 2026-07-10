from services.evaluator.ai_judge import AIJudge


class EvaluatorService:
    judge = AIJudge()

    @classmethod
    def evaluate(
        cls,
        question,
        answer,
        docs,
    ):

        context = "\n\n".join(doc.page_content for doc in docs)

        return cls.judge.evaluate(
            question,
            context,
            answer,
        )
