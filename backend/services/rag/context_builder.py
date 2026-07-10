from services.observability.decorators import measure_latency


class ContextBuilder:
    @staticmethod
    @measure_latency("context-builder")
    def build(docs):

        return "\n\n".join(doc.page_content for doc in docs)
