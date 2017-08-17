import os
import unittest
import json
from app import create_app, db
from app.models.models import User


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
        res = self.client().put('/bucketlists/1/items/1', data=self.item)
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/bucketlists/1/items', data=self.item)
        self.assertIn('test editing', str(results.data))

        # Test API can delete an existing bucketlist. (DELETE request)
        # Test search q  for non existing data
        res = self.client().get('/bucketlists/1/items?q=item5', data=self.item)
        self.assertIn('Items not found in the list', str(res.data))

        # Test search limit
        res = self.client().get('/bucketlists/1/items?limit=1', data=self.item)
        self.assertEqual(len(json.loads(res.data.decode())['items']), 1)

        # Test search limit with no numerical
        res = self.client().get('/bucketlists/1/items?limit=test', data=self.item)
        self.assertIn('Please pass a numeral.', json.loads(res.data.decode()).values())

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
