# tests/conftest.py
from datetime import datetime

import pytest
from alembic import command
from alembic.config import Config as AlembicConfig
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

from data.admin import create_admin
from database import api_get_session
from models import AccessPointModel, CustomerModel, TelemetryLogModel
from start_api import app
from tests.subscription_plans import create_subscription_plans

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
def seed_database(db):
    create_subscription_plans(db)
    parent_infra = AccessPointModel(id="IBAP", name="IBAP", device_order=1)
    parent_infra2 = AccessPointModel(id="IBAP2", name="IBAP2", device_order=1)
    db.add_all(
        [
            parent_infra,
            parent_infra2,
            AccessPointModel(id="AP1", name="AP1", parent=parent_infra, device_order=0),
            AccessPointModel(id="AP2", name="AP2", parent=parent_infra, device_order=0),
            AccessPointModel(
                id="AP3", name="AP3", parent=parent_infra2, device_order=0
            ),
            AccessPointModel(
                id="AP4", name="AP4", parent=parent_infra2, device_order=0
            ),
        ]
    )
    db.add_all(
        [
            CustomerModel(
                id="C2137",
                name="Customer 2137",
                access_point="AP1",
                subscription_plan_id=1,
            ),
            CustomerModel(
                id="C2138",
                name="Customer 2138",
                access_point="AP2",
                subscription_plan_id=2,
            ),
            CustomerModel(
                id="C2139",
                name="Customer 2139",
                access_point="AP4",
                subscription_plan_id=2,
            ),
            CustomerModel(
                id="C2140",
                name="Customer 2140",
                access_point="AP3",
                subscription_plan_id=2,
            ),
        ]
    )
    db.add_all(
        [
            TelemetryLogModel(
                access_point_id="AP3",
                start_date=datetime(2025, 1, 2, 0, 5, 3),
                end_date=datetime(2025, 1, 2, 0, 7, 3),
            ),
            TelemetryLogModel(
                access_point_id="IBAP2",
                start_date=datetime(2025, 1, 2, 0, 8, 3),
                end_date=datetime(2025, 1, 2, 0, 10, 3),
            ),
            TelemetryLogModel(
                access_point_id="IBAP2",
                start_date=datetime(2025, 1, 4, 0, 8, 3),
                end_date=datetime(2025, 1, 6, 0, 10, 3),
            ),
        ]
    )
    db.commit()
    yield db


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[api_get_session] = override_get_db
    with TestClient(app) as c:
        yield c
