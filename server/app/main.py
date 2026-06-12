from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import sessions

app = FastAPI(title="KimiNoteBook Session API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
