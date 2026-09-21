from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, insert, select, update

from config.db import conn
from middleware.auth import auth_required
from models.product import brands, categories, products
from schemas.product import ProductInput, ProductResponse

router = APIRouter()


def product_query():
    return (
        select(
            products,
            brands.c.id.label("brand_id_value"),
            brands.c.name.label("brand_name"),
            categories.c.id.label("category_id_value"),
            categories.c.name.label("category_name"),
        )
        .select_from(
            products.join(brands, products.c.brand_id == brands.c.id).join(
                categories, products.c.category_id == categories.c.id
            )
        )
    )


def serialize_product(row):
    data = dict(row._mapping)
    return {
        "id": data["id"],
        "name": data["name"],
        "brand_id": data["brand_id"],
        "category_id": data["category_id"],
        "image": data["image"],
        "qty": data["qty"],
        "price": data["price"],
        "brand": {"id": data["brand_id_value"], "name": data["brand_name"]},
        "category": {
            "id": data["category_id_value"],
            "name": data["category_name"],
        },
    }


def get_product(product_id: int):
    row = conn.execute(product_query().where(products.c.id == product_id)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize_product(row)


def validate_references(product: ProductInput):
    brand_exists = conn.execute(
        select(brands.c.id).where(brands.c.id == product.brand_id)
    ).first()
    category_exists = conn.execute(
        select(categories.c.id).where(categories.c.id == product.category_id)
    ).first()
    if brand_exists is None:
        raise HTTPException(status_code=400, detail="Brand not found")
    if category_exists is None:
        raise HTTPException(status_code=400, detail="Category not found")


@router.post("/product", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductInput, user=Depends(auth_required)):
    validate_references(product)
    result = conn.execute(insert(products).values(**product.model_dump()))
    conn.commit()
    return get_product(result.inserted_primary_key[0])


@router.get("/products", response_model=list[ProductResponse])
def get_products(user=Depends(auth_required)):
    rows = conn.execute(product_query()).fetchall()
    return [serialize_product(row) for row in rows]


@router.get("/product/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, user=Depends(auth_required)):
    return get_product(product_id)


@router.put("/product/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, product: ProductInput, user=Depends(auth_required)
):
    get_product(product_id)
    validate_references(product)
    conn.execute(
        update(products)
        .where(products.c.id == product_id)
        .values(**product.model_dump())
    )
    conn.commit()
    return get_product(product_id)


@router.delete("/product/{product_id}")
def delete_product(product_id: int, user=Depends(auth_required)):
    get_product(product_id)
    conn.execute(delete(products).where(products.c.id == product_id))
    conn.commit()
    return {"message": "Product deleted successfully"}
