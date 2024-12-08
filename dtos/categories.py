from typing import List, Optional
from pydantic import BaseModel

from dtos.products import ProductDto


class CategoryDto(BaseModel):
    id: int
    name: str
    description: str

    # Tämä on tuoteluettelo, ja se on valinnainen
    products: Optional[List[ProductDto]] = None


class CategoryDtoRes(BaseModel):
    id: int
    name: str
    description: str


class AddCategoryDtoReq(BaseModel):
    name: str
    description: str


class UpdateCategoryDtoReq(BaseModel):
    name: str
    description: str
