from typing import List, Optional
from pydantic import BaseModel

from dtos.products import ProductDto

class CategoryDto(BaseModel):
    id: int
    name: str
    description: str


