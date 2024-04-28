from ninja import Schema
from datetime import datetime


class OrderOut(Schema):
    id: int
    user_id: int
    total_price: float
    is_ordered: bool
    is_paid: bool
    is_delivered: bool
    date_ordered: datetime | None = None
    date_paid: datetime | None = None
    date_delivered: datetime | None = None

