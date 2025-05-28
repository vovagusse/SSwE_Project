import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from software_shop_webapp import db, model_queries


# ---------- Фикстуры ----------

@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def app_context(app):
    with app.app_context():
        yield


@pytest.fixture
def mock_product():
    product = MagicMock()
    product.product_id = 1
    product.id_developer = 42
    product.price = "1000"
    return product


@pytest.fixture
def mock_developer():
    developer = MagicMock()
    developer.developer_name = "Test Dev"
    return developer


# ---------- Тесты ----------

def test_get_products(app_context):
    with patch('software_shop_webapp.model_queries.Product.query') as mock_query:
        mock_query.all.return_value = ['prod1', 'prod2']
        result = model_queries.get_products()
        assert result == ['prod1', 'prod2']


def test_get_developer_names_for_product(app_context, mock_product, mock_developer):
    with patch('software_shop_webapp.model_queries.get_developer', return_value=mock_developer):
        result = model_queries.get_developer_names_for_product([mock_product])
        assert result == {1: "Test Dev"}


def test_get_first_image_for_product(app_context, mock_product):
    mock_image = MagicMock()
    with patch('software_shop_webapp.model_queries.get_images', return_value=[mock_image]):
        result = model_queries.get_first_image_for_product([mock_product])
        assert result == {1: mock_image}


def test_add_product_to_cart(app_context):
    with patch('software_shop_webapp.model_queries.db.session.execute') as mock_exec, \
         patch('software_shop_webapp.model_queries.db.session.commit') as mock_commit:
        model_queries.add_product_to_cart(1, 2)
        assert mock_exec.called
        assert mock_commit.called


def test_add_developer(app_context):
    with patch('software_shop_webapp.model_queries.db.session.execute') as mock_exec, \
         patch('software_shop_webapp.model_queries.db.session.commit') as mock_commit:
        model_queries.add_developer(1, "Developer X")
        assert mock_exec.called
        assert mock_commit.called


def test_get_products_in_cart(app_context):
    with patch('software_shop_webapp.model_queries.Product.query') as mock_query:
        mock_query.select_from.return_value.join.return_value.where.return_value.all.return_value = ['p1']
        result = model_queries.get_products_in_cart(1)
        assert result == ['p1']


def test_create_order(app_context):
    with patch('software_shop_webapp.model_queries.db.session.add') as mock_add, \
         patch('software_shop_webapp.model_queries.db.session.commit'):
        order = model_queries.create_order(123, 99.99)
        assert order.id_user == 123
        assert order.amount == 99.99
        assert order.status == "pending"


def test_process_order(app_context):
    mock_order = MagicMock()
    with patch('software_shop_webapp.model_queries.get_order', return_value=mock_order), \
         patch('software_shop_webapp.model_queries.db.session.commit') as mock_commit:
        model_queries.process_order("4111111111111111", 1)
        assert mock_order.card_number == "4111111111111111"
        assert mock_order.status == "success"
        assert mock_commit.called
