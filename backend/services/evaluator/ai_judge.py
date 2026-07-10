from services.evaluator.judge_result import JudgeResult
from services.llm.llm_factory import LLMFactory


class AIJudge:
    def __init__(self):

        self.provider = LLMFactory.get_provider()

    def evaluate(
        self,
        question,
        context,
        answer,
    ):
        prompt = f"""
You are an expert evaluator for Retrieval-Augmented Generation (RAG).

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Evaluate the generated answer.

Criteria:

1. Groundedness
- Is every factual statement supported by the retrieved context?

2. Hallucination
- Does the answer contain information that is NOT present in the context?

3. Faithfulness
- Score between 0 and 1.

4. Completeness
- Score between 0 and 1.

5. Relevance
- Score between 0 and 1.

Return ONLY valid JSON.

{{
    "grounded": true,
    "hallucination": false,
    "faithfulness": 0.95,
    "completeness": 0.90,
    "relevance": 0.98,
    "unsupported_claims": [],
    "reason": ""
}}
"""
        response = self.provider.generate(prompt)

        judge = JudgeResult.model_validate_json(response)
        return judge
