from fastapi import FastAPI

from src.docs.router import router as DocumnetRouter
from src.docs.es_service import AsyncESClient
from src.ingestion.router import router as IngestionRouter

app = FastAPI(
    title="Тестовое задание Python",
    description="Простой поисковик по текстам документов. Данные хранятся в БД" \
        "(PostgreSQL), поисковый индекс в ElasticSearch."
)

app.include_router(DocumnetRouter)
app.include_router(IngestionRouter)


@app.on_event("shutdown")
async def app_shutdown():
    await AsyncESClient().on_shutdown()
