import os
import unittest
import json
from app import create_app, db
from app.models.models import User


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'username': 'Test text', 'email': 'Test@text.com', 'password': 'Testtext'}
        self.bucketlist = {'name':'test bucketlist'}

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def test_bucketlist_creation_and_getting(self):
        """Test API can create a bucketlist (POST request)"""
        res = self.client().post('/bucketlists', data=self.bucketlist)
        self.assertEqual(res.status_code, 401)
        self.assertIn('token is missing!', str(res.data))

        # Test with valid token
        self.client().post('/auth/register', data=self.user)
        user = self.client().post('/auth/login', data=self.user)
        token = json.loads(user.data.decode())['token']
        self.bucketlist['auth-token'] = token
        res = self.client().post('/bucketlists', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('test bucketlist', str(json.loads(res.data.decode())['name']))

        # Test getting bucketlist from db
        res = self.client().get('/bucketlists', data=self.bucketlist)
        self.assertEqual(res.status_code, 200)
        self.assertIn('test bucketlist', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        self.client().post('/auth/register', data=self.user)
        user = self.client().post('/auth/login', data=self.user)
        print(user)
        token = json.loads(user.data.decode())['token']
        self.bucketlist['auth-token'] = token
        res = self.client().post('/bucketlists', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        id = json.loads(res.data.decode())['id']
        result = self.client().get(
            '/bucketlists/{}'.format(id), data=self.bucketlist)
        self.assertEqual(result.status_code, 200)
        self.assertIn('test bucketlist', str(result.data))

        # Test API can edit an existing bucketlist. (PUT request)
        self.bucketlist['name'] = 'new name'
        res = self.client().put('/bucketlists/1', data=self.bucketlist)
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/bucketlists/1', data=self.bucketlist)
        self.assertIn('new name', str(results.data))

        # Test API can delete an existing bucketlist. (DELETE request)
        res = self.client().delete('/bucketlists/1', data=self.bucketlist)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/bucketlists/1', data=self.bucketlist)
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


class ItemTestCase(unittest.TestCase):
    """This class represents the item test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'username': 'Test text', 'email': 'Test@text.com', 'password': 'Testtext'}
        self.bucketlist = {'name':'test bucketlist'}
        self.item = {'name': 'test item', 'description': 'This is a test', 'date': 'today'}

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def test_item_creation(self):
        """Test API can create a item (POST request)"""
        res = self.client().post('/bucketlists/1/items', data=self.item)
        self.assertEqual(res.status_code, 401)
        self.assertIn('token is missing!', str(res.data))

        # Test with valid token
        self.client().post('/auth/register', data=self.user)
        user = self.client().post('/auth/login', data=self.user)
        token = json.loads(user.data.decode())['token']
        self.bucketlist['auth-token'] = token
        res = self.client().post('/bucketlists', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('test bucketlist', str(json.loads(res.data.decode())['name']))
        self.item['auth-token'] = token
        res = self.client().post('/bucketlists/1/items', data=self.item)
        self.assertEqual(res.status_code, 201)
        self.assertIn('test item', str(json.loads(res.data.decode())['item_name']))

        # Test API can edit an existing bucketlist. (PUT request)
        self.item['item_name'] = 'test editing'
        # print(self.item)
        res = self.client().put('/bucketlists/1/items/1', data=self.item)
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/bucketlists/1/items', data=self.item)
        self.assertIn('test editing', str(results.data))

        # Test API can delete an existing bucketlist. (DELETE request)
        
        res = self.client().delete('/bucketlists/1/items/1', data=self.item)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/bucketlists/1/items/1', data=self.item)
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
