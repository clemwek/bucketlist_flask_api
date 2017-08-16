import os
import unittest
import json
from app import create_app, db
from app.models.models import User


class AuthTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'username': 'Test text', 'email': 'Test@text.com', 'password': 'Testtext'}

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def test_user_registration(self):
        """Test API can regisster a user (POST request)"""
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Test text', str(res.data))

    def test_user_login(self):
        """Test API can login a user (POST request)"""
        self.client().post('/auth/register', data=self.user)
        res = self.client().post('/auth/login', data=self.user)
        self.assertEqual(res.status_code, 202)
        self.assertIn('token', str(res.data))

        # Test for wrong password
        self.user['password'] = 'wrong'
        res = self.client().post('/auth/login', data=self.user)
        self.assertEqual(res.status_code, 401)
        self.assertIn('could not veryfy', str(res.data))

        # Test for non existing user
        self.user['username'] = 'wrong'
        res = self.client().post('/auth/login', data=self.user)
        self.assertEqual(res.status_code, 401)
        self.assertIn('could not veryfy', str(res.data))

    def test_user_logout(self):
        """Test API can logout a user (POST request)"""
        res = self.client().post('/auth/logout/', data=self.user)

    def test_user_password_reset(self):
        """Test API can reset password for a user (POST request)"""
        self.client().post('/auth/register', data=self.user)
        self.user['password'] = 'test2'
        res = self.client().post('/auth/reset-password', data=self.user)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/auth/login', data=self.user)
        self.assertEqual(res.status_code, 202)
        self.assertIn('token', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
