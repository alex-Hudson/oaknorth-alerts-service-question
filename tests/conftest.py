from typing import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from alerts_service import models, rest
from alerts_service.rest import get_session


@pytest.fixture(scope="session")
def engine() -> Engine:
    with PostgresContainer("postgres:16", driver="psycopg") as postgres_container:
        engine = create_engine(postgres_container.get_connection_url())
        yield engine


@pytest.fixture(scope="function")
def client():
    app = FastAPI()
    app.include_router(rest.router)
    return TestClient(app)


@pytest.fixture(scope="function")
def tables(engine: Engine) -> None:
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def session(client: TestClient, engine: Engine, tables: None) -> Session:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    def test_session() -> Iterator:
        yield session

    client.app.dependency_overrides[get_session] = test_session
    yield session
    client.app.dependency_overrides = {}
    session.close()
