'''we use pydantic classes to receive request body'''
from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    name: str
    description: Optional[str]
    price: float
    tax: Optional[float]
#   for python 3.10+
#   tax: float | None = None
