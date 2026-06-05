from fastapi import FastAPI

app = FastAPI(
    title="Study RAG Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Study RAG Platform API"
    }
