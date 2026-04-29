from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CreateProductPayload(BaseModel):
    name: str
    sku: str
    price: Decimal
    warehouse_id: int
    initial_quantity: int
    is_bundle: bool = False
    low_stock_threshold: int = 20

    model_config = ConfigDict(extra="forbid")
