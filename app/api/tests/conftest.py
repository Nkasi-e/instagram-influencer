from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.cors.database import Base, get_db
from app.cors.config import settings
from app.cors.security import create_access_token
from app.db.models.users import Profile
from app.main import app
import pytest


TEST_DATABASE = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(TEST_DATABASE, future=True)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(database):
    def override_get_db():
        try:
            yield database
        finally:
            database.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_create = {
        "email": "test@example.com",
        "password": "Password123",
    }
    res = client.post("/account/signup", json=user_create)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_create["password"]
    new_user["email"] = user_create["email"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_create = {
        "email": "test2@example.com",
        "password": "Password123",
    }
    res = client.post("/account/signup", json=user_create)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_create["password"]
    new_user["email"] = user_create["email"]
    return new_user


@pytest.fixture
def test_user3(client):
    user_create = {
        "email": "test3@example.com",
        "password": "Password123",
    }
    res = client.post("/account/signup", json=user_create)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_create["password"]
    new_user["email"] = user_create["email"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_user(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_profile(test_user, database, test_user2, test_user3):
    profile_data = [
        {
            "username": "snipes",
            "followers": 10,
            "bio": "Software Engineer",
            "owner_id": test_user["id"],
        },
        {
            "username": "dunks",
            "followers": 18,
            "bio": "I am a musical genius",
            "owner_id": test_user2["id"],
        },
        {
            "username": "coughs",
            "followers": 23,
            "bio": None,
            "owner_id": test_user3["id"],
        },
    ]

    def create_profile_model(profile):
        return Profile(**profile)

    profile_map = map(create_profile_model, profile_data)
    profiles = list(profile_map)
    database.add_all(profiles)
    database.commit()
    profiles = database.query(Profile).all()
    return profiles
