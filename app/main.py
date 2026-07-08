from fastapi import FastAPI
from app.adapters.api.v1.auth.router import router as auth_router
from app.adapters.api.v1.users.router import router as users_router
from app.adapters.api.v1.roles.router import router as roles_router
from app.adapters.api.v1.documents.router import router as documents_router



app = FastAPI(
    title="Study RAG Platform",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(documents_router)


@app.get("/")
def root():
    return {
        "message": "Study RAG Platform API"
    }
