import pytest
from app import app, db, PetProduct

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

@pytest.fixture
def session():
    with app.app_context():
        db.create_all()
        session = db.session

        yield session

        session.rollback()
        session.remove()
        db.drop_all()

def test_create_pet(client, session):
    session.begin_nested()
    response = client.post('/pets', json={'name': 'Cat', 'price': 10.99})
    assert response.status_code == 200
    assert response.json['message'] == 'Pet created successfully'
    response2 = client.get('/pets')
    assert response2.status_code == 200
    assert len(response2.json['pets']) == 1
    session.rollback()


def test_get_all_pets(client, session):
    session.begin_nested()
    client.post('/pets', json={'name': 'Cat', 'price': 10.99})
    client.post('/pets', json={'name': 'Dog', 'price': 15.99})
    response = client.get('/pets')
    assert response.status_code == 200
    assert len(response.json['pets']) == 2
    session.rollback()

def test_delete_pet(client, session):
    session.begin_nested()
    client.post('/pets', json={'name': 'Cat', 'price': 10.99})
    response1 = client.get('/pets')
    assert response1.status_code == 200
    assert len(response1.json['pets']) == 1
    client.delete(f'/pets/1')
    response2 = client.get('/pets')
    assert response2.status_code == 200
    assert len(response2.json['pets']) == 0
    session.rollback()