import unittest
from flask_api import app
from flask_api.models.models import User, Bucketlist, Item


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


class TestBucketlist(unittest.TestCase):
    def test_is_instance(self):
        new_bucketlist = Bucketlist('name')
        self.assertIsInstance(new_bucketlist, Bucketlist)


class TestBucketlistUrl(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_protected_urls(self):
        bucketlists_post = self.client.post('/bucketlists')
        bucketlists_get = self.client.get('/bucketlists')
        self.assertEqual(bucketlists_post.status_code, 200)
        self.assertEqual(bucketlists_get.status_code, 200)
