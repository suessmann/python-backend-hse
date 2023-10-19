import pytest
from app import app, db, Product
from unittest.mock import patch

# Http Client mock
@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

# Test for creating product
@patch('app.db.session')
def test_create_product(mock_session, client):
    mock_session.add.return_value = None

    response = client.post('/products', json={'name': 'Cat', 'price': 10.99})
    assert response.status_code == 200
    assert response.json['message'] == 'Product created successfully'

    mock_session.add.assert_called_once()


# Test for get all product with mock
@patch('app.db.session')
def test_get_all_products(mock_session, client):
    mock_products = [
        Product(name='Cat', price=10.99),
        Product(name='Dog', price=15.99)
    ]
    mock_session.query.return_value.all = mock_products

    response = client.get('/products')
    assert response.status_code == 200

    mock_session.assert_called_once()

# Test for updating product
@patch('app.db.session')
def test_update_product(mock_session, client):
    mock_product = Product(name='Cat', price=10.99)
    mock_session.query.return_value.get.return_value = mock_product

    response = client.put('/products/1', json={'name': 'Kitten', 'price': 12.99})
    assert response.status_code == 200
    assert response.json['message'] == 'Product updated successfully'

    mock_session.assert_called_once_with()
