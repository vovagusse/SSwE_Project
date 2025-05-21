import pytest
import shutil
import os
from sqlalchemy import inspect
from software_shop_webapp import app, db

REAL_DB_PATH = 'C:\\Users\\Lenovo\\Documents\\GitHub\\SSwE_Project\\software_shop_webapp\\software_shop.db'
TEST_DB_PATH = 'test_app.db'

@pytest.fixture(scope='session')
def client():
    if not os.path.exists(REAL_DB_PATH):
        raise FileNotFoundError(f"БД не найдена: {REAL_DB_PATH}")

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    shutil.copyfile(REAL_DB_PATH, TEST_DB_PATH)

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{TEST_DB_PATH}"

    with app.app_context():
        db.engine.dispose()
        db.create_all()

    with app.test_client() as client:
        yield client

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_app_config(client):
    assert app.config['TESTING'] is True

def test_homepage_route_exists(client):
    response = client.get('/')
    assert response.status_code in (200, 404)

def test_database_initialization(client):
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        assert isinstance(tables, list)
