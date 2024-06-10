from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Borrower(BaseModel):
    borrower_id: int
    name: str
    last_modified: datetime
    total_revenue: Optional[float] = None
    ebitda: Optional[float] = None
    dscr: Optional[float] = None
    debt_to_ebitda: Optional[float] = None


class BorrowerCreate(BaseModel):
    name: str
    total_revenue: Optional[float] = None
    ebitda: Optional[float] = None
    dscr: Optional[float] = None
    debt_to_ebitda: Optional[float] = None


class Operator(str, Enum):
    gt = "gt"
    eq = "eq"
    lt = "lt"


class Alert(BaseModel):
    alert_id: int
    data_item: str
    operator: Operator
    value: float
    last_modified: datetime


class AlertCreate(BaseModel):
    data_item: str
    operator: Operator
    value: float
