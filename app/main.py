from fastapi import FastAPI

from app.adapters.http.routes.chat_routes import (
    router as chat_router,
)
from app.adapters.http.routes.document_routes import (
    router as document_router,
)
from app.adapters.http.routes.exam_routes import (
    router as exam_router,
)
from app.adapters.http.routes.flashcard_routes import (
    router as flashcard_router,
)
from app.adapters.http.routes.study_room_routes import (
    router as study_room_router,
)
from app.config.settings import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.include_router(document_router)
app.include_router(study_room_router)
app.include_router(chat_router)
app.include_router(flashcard_router)
app.include_router(exam_router)


@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} API",
    }
