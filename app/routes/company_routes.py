from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.company_controllers import get_low_stock_alerts
from app.db.session import get_db
from app.schemas.company_schemas import LowStockAlertsResponse

router = APIRouter(prefix="/api/companies", tags=["companies"])


@router.get("/{company_id}/alerts/low-stock", response_model=LowStockAlertsResponse)
def low_stock_alerts(company_id: int, db: Session = Depends(get_db)) -> LowStockAlertsResponse:
    return get_low_stock_alerts(company_id=company_id, db=db)
