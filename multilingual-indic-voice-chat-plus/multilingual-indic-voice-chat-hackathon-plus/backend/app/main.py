
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chat import router as chat_router
from app.routers.health import router as health_router
from app.routers.asr_tts import router as media_router
from app.routers.kb import router as kb_router
from app.middleware.api_key import api_key_middleware

app = FastAPI(title="Indic Voice Chat (Hackathon+)", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware('http')(api_key_middleware)

app.include_router(chat_router, prefix="/api/v1")
app.include_router(media_router, prefix="/api/v1")
app.include_router(kb_router, prefix="/api/v1")
app.include_router(health_router)
