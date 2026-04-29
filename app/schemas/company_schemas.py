from typing import Optional

from pydantic import BaseModel


class SupplierAlertInfo(BaseModel):
    id: int
    name: str
    contact_email: Optional[str] = None


class LowStockAlertItem(BaseModel):
    product_id: int
    product_name: str
    sku: str
    warehouse_id: int
    warehouse_name: str
    current_stock: int
    threshold: int
    days_until_stockout: Optional[int] = None
    supplier: Optional[SupplierAlertInfo] = None


class LowStockAlertsResponse(BaseModel):
    alerts: list[LowStockAlertItem]
    total_alerts: int
