class ResponseBuilder:

    @staticmethod
    def build(answer: str, docs: list):
        """
        Builds the API response.

        Responsibilities
        ----------------
        • Remove duplicate sources
        • Build response object
        • Keep response format consistent
        """

        unique_sources = []
        seen = set()

        for doc in docs:

            key = (
                doc.metadata.get("source"),
                doc.metadata.get("page"),
            )

            if key not in seen:
                seen.add(key)

                unique_sources.append(
                    {
                        "file": key[0],
                        "page": key[1],
                    }
                )

        return {
            "Answer": answer,
            "Source": unique_sources,
        }