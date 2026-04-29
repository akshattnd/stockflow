from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Inventory, Product, Warehouse
from app.schemas.products_schemas import CreateProductPayload


def create_product_with_inventory(payload: CreateProductPayload, db: Session) -> dict:
    warehouse = db.query(Warehouse).filter(Warehouse.id == payload.warehouse_id).first()
    if warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found",
        )

    existing_sku = db.query(Product).filter(Product.sku == payload.sku).first()
    if existing_sku is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="SKU already exists",
        )

    product = Product(
        name=payload.name,
        sku=payload.sku,
        price=payload.price,
        is_bundle=payload.is_bundle,
        low_stock_threshold=payload.low_stock_threshold,
    )
    db.add(product)
    db.flush()

    inventory = Inventory(
        product_id=product.id,
        warehouse_id=payload.warehouse_id,
        quantity=payload.initial_quantity,
    )
    db.add(inventory)
    db.commit()

    return {"message": "Product created", "product_id": product.id}
