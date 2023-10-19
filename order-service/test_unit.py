import pytest
from app import app, db, Order
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

# Test for creating order
@patch('app.db.session')
def test_create_order(mock_session, client):
    mock_session.add.return_value = None

    response = client.post('/orders', json={'status': 'CREATED', 'total_price': 10.99})
    assert response.status_code == 200
    assert response.json['message'] == 'Order created successfully'

    mock_session.add.assert_called_once()


# Test for get all order with mock
@patch('app.db.session')
def test_get_all_orders(mock_session, client):
    mock_orders = [
        Order(status='CREATED', total_price=10.99),
        Order(status='SHIPPED', total_price=15.99)
    ]
    mock_session.query.return_value.all = mock_orders

    response = client.get('/orders')
    assert response.status_code == 200

    mock_session.assert_called_once()

# Test for updating order
@patch('app.db.session')
def test_update_order(mock_session, client):
    mock_order = Order(status='CREATED', total_price=10.99)
    mock_session.query.return_value.get.return_value = mock_order

    response = client.put('/orders/1', json={'status': 'Kitten', 'total_price': 12.99})
    assert response.status_code == 200
    assert response.json['message'] == 'Order updated successfully'

    mock_session.assert_called_once_with()
