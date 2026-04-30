import pytest
import os
import sqlite3
from app import app
import database

@pytest.fixture
def client():
    # use test database
    os.environ["DB_NAME"] = "test.db"

    # delete old DB if exists
    if os.path.exists("test.db"):
        os.remove("test.db")

    # initialize fresh DB
    database.init_db()

    # create test client
    with app.test_client() as client:
        yield client

    try:
        sqlite3.connect("test.db").close()
    except:
        pass


def test_register(client):
    res = client.post("/register", json={
        "username": "user1",
        "email": "user1@test.com"
    })

    assert res.status_code == 201
    assert "password" in res.get_json()


def test_auth_success(client):
    res = client.post("/register", json={
        "username": "user2",
        "email": "user2@test.com"
    })

    password = res.get_json()["password"]

    res2 = client.post("/auth", json={
        "username": "user2",
        "password": password
    })

    assert res2.status_code == 200


def test_auth_fail(client):
    res = client.post("/auth", json={
        "username": "fake",
        "password": "wrong"
    })

    assert res.status_code == 401


def test_jwks(client):
    res = client.get("/jwks")

    assert res.status_code == 200
    assert "keys" in res.get_json()