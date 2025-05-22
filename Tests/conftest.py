import pytest
import shutil
import os
from software_shop_webapp import app, db

REAL_DB_PATH = 'software_shop_webapp\\software_shop.db'
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

@pytest.fixture(scope='function')
def app_context():
    """Фикстура для предоставления контекста приложения в тестах"""
    with app.app_context():
        yield
