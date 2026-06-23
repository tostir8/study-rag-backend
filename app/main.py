from fastapi import FastAPI
from app.adapters.api.v1.auth.router import router as auth_router


app = FastAPI(
    title="Study RAG Platform",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "Study RAG Platform API"
    }
