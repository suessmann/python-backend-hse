import unittest
from app import app


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_register(self):
        response = self.app.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        self.app.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)

    def test_login_invalid_username(self):
        response = self.app.post('/login', json={'username': 'nonexistentuser', 'password': 'testpassword'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Invalid username')

    def test_login_invalid_password(self):
        self.app.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'wrongpassword'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Invalid password')


if __name__ == '__main__':
    unittest.main()
