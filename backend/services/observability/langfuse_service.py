import os
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


class LangfuseService:
    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:
            cls._client = Langfuse(
                secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                host=os.getenv(
                    "LANGFUSE_HOST",
                    "https://cloud.langfuse.com",
                ),
            )

        return cls._client
