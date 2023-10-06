import pytest
from app import app, db, PetProduct
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

@patch('app.db.session')
def test_create_pet(mock_session, client):
    mock_session.add.return_value = None

    response = client.post('/pets', json={'name': 'Cat', 'price': 10.99})
    assert response.status_code == 200
    assert response.json['message'] == 'Pet created successfully'

    mock_session.add.assert_called_once()


@patch('app.db.session')
def test_get_all_pets(mock_session, client):
    mock_pets = [
        PetProduct(name='Cat', price=10.99),
        PetProduct(name='Dog', price=15.99)
    ]
    mock_session.query.return_value.all = mock_pets

    response = client.get('/pets')
    assert response.status_code == 200

    mock_session.assert_called_once()

@patch('app.db.session')
def test_update_pet(mock_session, client):
    mock_pet = PetProduct(name='Cat', price=10.99)
    mock_session.query.return_value.get.return_value = mock_pet

    response = client.put('/pets/1', json={'name': 'Kitten', 'price': 12.99})
    assert response.status_code == 200
    assert response.json['message'] == 'Pet updated successfully'

    mock_session.assert_called_once_with()
