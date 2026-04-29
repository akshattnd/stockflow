from fastapi import FastAPI

from app.routes.products_routes import router as products_router

app = FastAPI(title="Stockflow API")

app.include_router(products_router)
