# tests/conftest.py

import pytest
from alembic import command
from alembic.config import Config as AlembicConfig
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

from data.admin import create_admin
from database import api_get_session
from start_api import app
from tests.data.subscription_plans import create_subscription_plans

TEST_DATABASE_URL = "sqlite:///./test.db"  # Change to Postgres URL for real integration
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)


def run_migrations():
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")


def clean_db(session):
    session.execute(text("PRAGMA foreign_keys = OFF;"))  # Only for SQLite

    inspector = inspect(session.bind)
    table_names = inspector.get_table_names()

    for table in table_names:
        if table != "alembic_version":
            session.execute(text(f'DELETE FROM "{table}";'))

    session.commit()
    session.execute(text("PRAGMA foreign_keys = ON;"))  # Only for SQLite


@pytest.fixture(scope="function")
def db():
    run_migrations()
    session = TestingSessionLocal()
    create_subscription_plans(session)
    create_admin(
        session,
        login="admin",
        password="admintest",
    )
    yield session
    clean_db(session)
    session.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[api_get_session] = override_get_db
    with TestClient(app) as c:
        yield c
