from fastapi import APIRouter, UploadFile

from services.upload.upload_service import UploadService

router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile):
    """
    Upload Endpoint

    Responsibility:
    ----------------
    1. Receive the uploaded file
    2. Pass it to UploadService
    3. Return the response

    NOTE:
    This router should NEVER contain
    business logic like:

    ❌ PDF Loading
    ❌ Chunking
    ❌ Embedding
    ❌ Vector Indexing

    Those belong inside UploadService.
    """

    return await UploadService.upload(file)
