from fastapi import UploadFile

from services.chunk.chunk_service import ChunkService
from services.embedding.embedding_service import EmbeddingService
from services.loaders.loader_factory import LoaderFactory
from services.vector_store.vector_store import VectorStore
from config.setting import settings


class UploadService:
    @staticmethod
    async def upload(file: UploadFile):
        """
        Upload Workflow

        Step 1
            Save uploaded PDF

        Step 2
            Load PDF into LangChain Documents

        Step 3
            Add metadata to every page

        Step 4
            Split document into chunks

        Step 5
            Load embedding model

        Step 6
            Generate embeddings

        Step 7
            Store embeddings inside ChromaDB

        Return
            Success response
        """

        # ---------------------------------------------------------
        # Step 1 : Save Uploaded File
        # ---------------------------------------------------------

        file_path = f"{settings.UPLOAD_DIR}/{file.filename}"

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # ---------------------------------------------------------
        # Step 2 : Load PDF
        # ---------------------------------------------------------

        documents = LoaderFactory.load(file_path)
        print("=" * 80)
        print("Pages:", len(documents))

        for i, doc in enumerate(documents[:3]):
            print(f"\nPAGE {i}")
            print(doc.page_content[:500])
        # ---------------------------------------------------------
        # Step 3 : Add Metadata
        #
        # Metadata is used later for:
        # - Source Selection
        # - Multi PDF Retrieval
        # - Citations
        # ---------------------------------------------------------

        for doc in documents:
            doc.metadata["source"] = file.filename

        # ---------------------------------------------------------
        # Step 4 : Chunking
        # ---------------------------------------------------------

        chunks = ChunkService.split(documents)
        print("=" * 80)
        print("Chunks:", len(chunks))

        for i, chunk in enumerate(chunks[:5]):
            print(f"\nCHUNK {i}")
            print(chunk.page_content[:300])
        # ---------------------------------------------------------
        # Step 5 : Load Embedding Model
        # ---------------------------------------------------------

        embedding = EmbeddingService.get_model()

        # ---------------------------------------------------------
        # Step 6 : Create Vector Index
        # ---------------------------------------------------------

        VectorStore.create(chunks, embedding)

        # ---------------------------------------------------------
        # Step 7 : Response
        # ---------------------------------------------------------

        return {"message": f"{file.filename} indexed successfully."}
