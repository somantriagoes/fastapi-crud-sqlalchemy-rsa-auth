from pydantic import BaseModel, ConfigDict


class ProductInput(BaseModel):
    name: str
    brand_id: int
    category_id: int
    image: str | None = None
    qty: int = 0
    price: float


class BrandResponse(BaseModel):
    id: int
    name: str | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str | None = None


class ProductResponse(ProductInput):
    model_config = ConfigDict(from_attributes=True)

    id: int
    brand: BrandResponse
    category: CategoryResponse
