from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.routes.company_routes import router as company_router
from app.routes.products_routes import router as products_router

app = FastAPI(title="Stockflow API")


@app.on_event("startup")
def create_database_tables() -> None:
    # Ensure all registered models have corresponding tables at startup.
    Base.metadata.create_all(bind=engine)


app.include_router(products_router)
app.include_router(company_router)
