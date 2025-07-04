from fastapi import FastAPI
from app.endpoints import router as api_router

app = FastAPI(title="Excel Processor Assignment", docs_url="/", redoc_url=None)

app.include_router(api_router)
