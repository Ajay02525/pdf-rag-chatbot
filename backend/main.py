from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
from services.startup.lifespan import lifespan
from prometheus_client import make_asgi_app

from api.routes.ask import router as ask_router
from api.routes.upload import router as upload_router
from services.observability.middleware import metrics_middleware
from api.routes.system import router as system_router
from fastapi.middleware.cors import CORSMiddleware
from config.setting import settings
from pathlib import Path

Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.CHROMA_DIR).mkdir(parents=True, exist_ok=True)

app = FastAPI(lifespan=lifespan)
origins = [
    settings.FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(metrics_middleware)
metrics_app = make_asgi_app()

app.mount(
    "/metrics",
    metrics_app,
)
app.include_router(system_router)
app.include_router(upload_router)
app.include_router(ask_router)


@app.get("/stream-test")
async def stream_test():
    async def generate():
        for i in range(10):
            yield f"Chunk {i}\n"
            await asyncio.sleep(1)

    return StreamingResponse(generate(), media_type="text/plain")


# @app.post("/ask")
# async def ask(req: AskRequest):
#     return await RAGService.ask(
#         question=req.question,
#         session_id=req.session_id,
#     )
