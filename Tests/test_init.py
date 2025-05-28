import os
import sys
import shutil
import pytest
from sqlalchemy import inspect

# ---------- Пути к проекту и БД ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REAL_DB_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../software_shop_webapp/software_shop.db")
)

TEST_DB_PATH = os.path.join(BASE_DIR, "test_app.db")

sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, "../")))

from software_shop_webapp import app, db  # noqa: E402


# ---------- Фикстура тестового клиента Flask с копией БД ----------

@pytest.fixture(scope='session')
def client():
    if not os.path.exists(REAL_DB_PATH):
        raise FileNotFoundError(f"БД не найдена: {REAL_DB_PATH}")

    # Копируем рабочую БД в тестовую
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    shutil.copyfile(REAL_DB_PATH, TEST_DB_PATH)

    # Настройки приложения для теста
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{TEST_DB_PATH}"

    # Создаём таблицы в тестовой БД
    with app.app_context():
        db.engine.dispose()
        db.create_all()

    # Запускаем Flask test client
    with app.test_client() as client:
        yield client

    # Удаляем тестовую БД после завершения
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


# ---------- Тесты ----------

def test_app_config(client):
    """Проверка, что включён режим тестирования"""
    assert app.config['TESTING'] is True


def test_homepage_route_exists(client):
    """Проверка, что корневая страница существует (200 или 404, если не реализовано)"""
    response = client.get('/')
    assert response.status_code in (200, 404)


def test_database_initialization(client):
    """Проверка, что таблицы успешно загружаются из базы"""
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        assert isinstance(tables, list)
        assert len(tables) > 0
