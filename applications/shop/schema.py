from ninja import Schema
from datetime import datetime
from typing import List
from pydantic.fields import Field


class Error(Schema):
    code: str
    message: str


class CategoryOut(Schema):
    id: int
    name: str
    description: str | None = None


class ProductIn(Schema):
    name: str
    description: str
    price: float
    category: int


class ProductOut(Schema):
    id: int
    category_id: int
    name: str
    description: str
    price: float
    image: str | None = None
    date_created: datetime
    date_updated: datetime


class ProductFilters(Schema):
    categories: List[str] = Field(None, alias="categories")


class CartOut(Schema):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    product: ProductOut
