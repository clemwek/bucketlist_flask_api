import unittest
from flask_api.flask_api import app
from flask_api.models.bucketlist.bucketlist import Bucketlist


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
