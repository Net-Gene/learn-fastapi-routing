from pydantic import BaseModel

class ProductDto(BaseModel):
    id: int
    name: str
    unit_price: int
    description: str

