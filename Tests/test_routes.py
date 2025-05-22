import pytest
from unittest.mock import patch
import os
import sys
sys.path.insert(0, os.path.abspath("../"))                     #Those two lines do
# sys.path.insert(0, os.path.abspath("../../software_shop_webapp")) #Some Fucking Magic
from software_shop_webapp import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_login_page_get(client):
    """Тестируем, что GET /login/ возвращает страницу с кодом 200"""
    response = client.get('/login/')
    assert response.status_code == 200
    page_text = response.data.decode('utf-8')
    # Проверяем наличие текста "Вход" или "login" в ответе
    assert "Вход" in page_text or "login" in page_text.lower()

