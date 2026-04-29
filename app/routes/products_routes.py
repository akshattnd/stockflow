from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.products_controllers import create_product_with_inventory
from app.db.session import get_db
from app.schemas.products_schemas import CreateProductPayload

router = APIRouter(prefix="/api/products", tags=["products"])


@router.post("")
def create_product(payload: CreateProductPayload, db: Session = Depends(get_db)) -> dict:
    return create_product_with_inventory(payload=payload, db=db)
