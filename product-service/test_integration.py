import pytest
from app import app, db, Product


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


# DB Session mock
@pytest.fixture
def session():
    with app.app_context():
        db.create_all()
        session = db.session

        yield session

        session.rollback()
        session.remove()
        db.drop_all()


# Test for creating product
def test_create_product(client, session):
    session.begin_nested()
    response = client.post('/products', json={'name': 'Cat', 'price': 10.99})
    assert response.status_code == 200
    assert response.json['message'] == 'Product created successfully'
    response2 = client.get('/products')
    assert response2.status_code == 200
    assert len(response2.json['products']) == 1
    session.rollback()


# Test for getting list of products using db
def test_get_all_products(client, session):
    session.begin_nested()
    client.post('/products', json={'name': 'Cat', 'price': 10.99})
    client.post('/products', json={'name': 'Dog', 'price': 15.99})
    response = client.get('/products')
    assert response.status_code == 200
    assert len(response.json['products']) == 2
    session.rollback()


# Test for deleting product using db
def test_delete_product(client, session):
    session.begin_nested()
    client.post('/products', json={'name': 'Cat', 'price': 10.99})
    response1 = client.get('/products')
    assert response1.status_code == 200
    assert len(response1.json['products']) == 1
    client.delete(f'/products/1')
    response2 = client.get('/products')
    assert response2.status_code == 200
    assert len(response2.json['products']) == 0
    session.rollback()
