from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json
from models.ask_request import AskRequest
from services.rag.rag_service import RAGService

router = APIRouter()


@router.post("/ask")
async def ask(req: AskRequest):
    """
    Ask Router

    Responsibilities
    ----------------
    ✔ Receive HTTP Request
    ✔ Validate Request
    ✔ Call RAGService
    ✔ Return Response

    No business logic should live here.
    """

    async def event_generator():
        async for event in RAGService.ask(
            question=req.question,
            session_id=req.session_id,
        ):
            yield f"data: {json.dumps(event)}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
