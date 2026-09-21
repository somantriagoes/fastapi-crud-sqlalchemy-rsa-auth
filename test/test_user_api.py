import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from main import app
import api.user as api_user
from config import db as db_module


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
    api_user.conn = conn
    db_module.meta.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    conn.close()


def test_create_and_list_users(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "secret123",
    }

    create_response = client.post("/user", json=payload)
    assert create_response.status_code == 200
    created_users = create_response.json()
    assert len(created_users) == 1
    assert created_users[0]["name"] == payload["name"]
    assert created_users[0]["email"] == payload["email"]
    assert created_users[0]["password"] == payload["password"]

    list_response = client.get("/users")
    assert list_response.status_code == 200
    assert list_response.json()[0]["email"] == payload["email"]


def test_create_user_is_persisted_to_database(tmp_path):
    db_file = tmp_path / "users.db"
    engine = create_engine(f"sqlite:///{db_file}")
    conn = engine.connect()
    db_module.engine = engine
    db_module.conn = conn
    api_user.conn = conn
    db_module.meta.create_all(bind=engine)

    with TestClient(app) as test_client:
        response = test_client.post(
            "/user",
            json={
                "name": "Persisted User",
                "email": "persisted@example.com",
                "password": "persisted-pass",
            },
        )

        assert response.status_code == 200

        fresh_conn = engine.connect()
        rows = fresh_conn.execute(db_module.meta.tables["users"].select()).fetchall()
        assert len(rows) == 1
        assert rows[0][1] == "Persisted User"
        fresh_conn.close()

    conn.close()


def test_get_user_by_id(client):
    client.post(
        "/user",
        json={
            "name": "Bob",
            "email": "bob@example.com",
            "password": "pass456",
        },
    )

    response = client.get("/user/1")
    assert response.status_code == 200
    user = response.json()[0]
    assert user["name"] == "Bob"
    assert user["email"] == "bob@example.com"


def test_update_user(client):
    client.post(
        "/user",
        json={
            "name": "Carol",
            "email": "carol@example.com",
            "password": "oldpass",
        },
    )

    response = client.put(
        "/user/1",
        json={
            "name": "Carol Updated",
            "email": "carol.updated@example.com",
            "password": "newpass",
        },
    )

    assert response.status_code == 200
    updated_user = response.json()[0]
    assert updated_user["name"] == "Carol Updated"
    assert updated_user["email"] == "carol.updated@example.com"
    assert updated_user["password"] == "newpass"


def test_delete_user(client):
    client.post(
        "/user",
        json={
            "name": "Dave",
            "email": "dave@example.com",
            "password": "delete-me",
        },
    )

    response = client.delete("/user/1")
    assert response.status_code == 200
    assert response.json() == []
