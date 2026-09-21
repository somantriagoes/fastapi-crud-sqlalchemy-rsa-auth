import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, insert
from sqlalchemy.pool import StaticPool

from main import app
import api.product as api_product
from config import db as db_module
from middleware.auth import auth_required
from models.product import brands, categories


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    conn = engine.connect()
    db_module.engine = engine
    db_module.conn = conn
    api_product.conn = conn
    db_module.meta.create_all(bind=engine)
    conn.execute(insert(brands).values(id=1, name="CIDEA"))
    conn.execute(insert(categories).values(id=1, name="FROZEN"))
    conn.commit()

    app.dependency_overrides[auth_required] = lambda: {"id": 1}
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    conn.close()


PRODUCT_PAYLOAD = {
    "name": "Frozen Food",
    "brand_id": 1,
    "category_id": 1,
    "image": "assets/images/image.jpg",
    "qty": 100,
    "price": 12000.00,
}


def test_product_endpoints_require_token():
    app.dependency_overrides.clear()
    response = TestClient(app).get("/api/products")
    assert response.status_code == 401


def test_create_product(client):
    response = client.post("/api/product", json=PRODUCT_PAYLOAD)
    assert response.status_code == 201
    assert response.json()["name"] == "Frozen Food"


def test_get_all_products(client):
    client.post("/api/product", json=PRODUCT_PAYLOAD)
    response = client.get("/api/products")
    assert response.status_code == 200
    product = response.json()[0]
    assert product["brand"] == {"id": 1, "name": "CIDEA"}
    assert product["category"] == {"id": 1, "name": "FROZEN"}


def test_get_product_by_id(client):
    client.post("/api/product", json=PRODUCT_PAYLOAD)
    response = client.get("/api/product/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_update_product(client):
    client.post("/api/product", json=PRODUCT_PAYLOAD)
    updated_payload = {**PRODUCT_PAYLOAD, "name": "Frozen Food Rasa Ayam Gulai"}
    response = client.put("/api/product/1", json=updated_payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Frozen Food Rasa Ayam Gulai"


def test_delete_product(client):
    client.post("/api/product", json=PRODUCT_PAYLOAD)
    response = client.delete("/api/product/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}
    assert client.get("/api/products").json() == []
