from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import Company, Inventory, Product, Supplier, SupplierProduct, Warehouse
from app.schemas.company_schemas import (
    LowStockAlertItem,
    LowStockAlertsResponse,
    SupplierAlertInfo,
)


def _has_recent_sales_activity(product_id: int, db: Session) -> bool:
    """
    Assumption: no sales/order table exists yet in the current schema.
    To keep this endpoint usable, every product is treated as recently active.
    Replace this with a real 30-day sales join once sales models are added.
    """
    _ = (product_id, db)
    return True


def _estimate_days_until_stockout(product_id: int, current_stock: int, db: Session) -> Optional[int]:
    """
    Assumption: there is no sales velocity source in the current schema.
    We return None rather than a fabricated estimate.
    """
    _ = (product_id, current_stock, db)
    return None


def get_low_stock_alerts(company_id: int, db: Session) -> LowStockAlertsResponse:
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    inventory_rows = (
        db.query(Inventory, Product, Warehouse)
        .join(Product, Product.id == Inventory.product_id)
        .join(Warehouse, Warehouse.id == Inventory.warehouse_id)
        .filter(Warehouse.company_id == company_id)
        .all()
    )

    if not inventory_rows:
        return LowStockAlertsResponse(alerts=[], total_alerts=0)

    product_ids = list({product.id for _, product, _ in inventory_rows})
    supplier_rows = (
        db.query(SupplierProduct, Supplier)
        .join(Supplier, Supplier.id == SupplierProduct.supplier_id)
        .filter(SupplierProduct.product_id.in_(product_ids))
        .order_by(SupplierProduct.product_id, SupplierProduct.cost_price, Supplier.id)
        .all()
    )

    primary_supplier_by_product: dict[int, Supplier] = {}
    for supplier_product, supplier in supplier_rows:
        if supplier_product.product_id not in primary_supplier_by_product:
            primary_supplier_by_product[supplier_product.product_id] = supplier

    alerts: list[LowStockAlertItem] = []
    for inventory, product, warehouse in inventory_rows:
        threshold = product.low_stock_threshold
        if inventory.quantity >= threshold:
            continue

        if not _has_recent_sales_activity(product.id, db):
            continue

        supplier = primary_supplier_by_product.get(product.id)
        supplier_payload = (
            SupplierAlertInfo(
                id=supplier.id,
                name=supplier.name,
                contact_email=supplier.contact_email,
            )
            if supplier is not None
            else None
        )

        alerts.append(
            LowStockAlertItem(
                product_id=product.id,
                product_name=product.name,
                sku=product.sku,
                warehouse_id=warehouse.id,
                warehouse_name=warehouse.name,
                current_stock=inventory.quantity,
                threshold=threshold,
                days_until_stockout=_estimate_days_until_stockout(
                    product_id=product.id,
                    current_stock=inventory.quantity,
                    db=db,
                ),
                supplier=supplier_payload,
            )
        )

    return LowStockAlertsResponse(alerts=alerts, total_alerts=len(alerts))
