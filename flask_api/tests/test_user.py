import unittest
from flask_api.models.users.user import User
from flask_api.flask_api import app


class TestUser(unittest.TestCase):
    def test_is_instance(self):
        new_user = User('name', 'username', 'email@test.com', 'password')
        self.assertIsInstance(new_user, User)


class TestUserViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_public_url(self):
        register = self.client.post('/auth/register')
        self.assertEqual(register.status_code, 200)

        login = self.client.post('/auth/login')
        self.assertEqual(login.status_code, 200)

        logout = self.client.post('/auth/logout')
        self.assertEqual(logout.status_code, 200)

        reset_password = self.client.post('/auth/reset_password')
        self.assertEqual(reset_password.status_code, 200)
