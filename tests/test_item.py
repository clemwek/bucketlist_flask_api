"""
This tests the functions in the items view
"""


import unittest
import json
from app import create_app, db


class ItemTestCase(unittest.TestCase):
    """This class represents the item test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'username': 'Test text', 'email': 'Test@text.com', 'password': 'Testtext'}
        self.bucketlist = {'name':'test bucketlist'}
        self.item = {'name': 'test item', 'description': 'This is a test', 'date': '08/05/2017'}

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def valid_token(self):
        self.client().post('/auth/register', data=self.user)
        user = self.client().post('/auth/login', data=self.user)
        token = json.loads(user.data.decode())['token']
        return {'Authorization': token}

    def test_item_creation_without_token(self):
        """Test API can create a item (POST request)"""
        res = self.client().post('/bucketlists/1/items', data=self.item)
        self.assertEqual(res.status_code, 401)
        self.assertIn('token is missing!', str(res.data))

    def test_item_creation(self):
        # Test with valid token
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        res = self.client().post('/bucketlists/1/items', headers=self.valid_token(), data=self.item)
        self.assertEqual(res.status_code, 201)
        self.assertIn('test item', str(json.loads(res.data.decode())['name']))

    def test_item_creation_with_invalid_date(self):
        # Test for incorrect date format
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        self.item['date'] = 'today'
        res = self.client().post('/bucketlists/1/items', headers=self.valid_token(), data=self.item)
        self.assertEqual(res.status_code, 403)
        self.assertIn('date is not valid', str(res.data))

    def test_item_creation_with_missing_data(self):
        # Test for missing data
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        self.item['date'] = ''
        res = self.client().post('/bucketlists/1/items', headers=self.valid_token(), data=self.item)
        self.assertEqual(res.status_code, 403)
        self.assertIn('Some data is missing!', str(res.data))

    def test_editing_item(self):
        # Test API can edit an existing bucketlist. (PUT request)
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        res = self.client().post(
            '/bucketlists/1/items', headers=self.valid_token(), data=self.item)
        self.item['name'] = 'test editing'
        res = self.client().put(
            '/bucketlists/1/items/1', headers=self.valid_token(), data=self.item)
        self.assertEqual(res.status_code, 200)
        results = self.client().get(
            '/bucketlists/1/items/1', headers=self.valid_token(), data=self.item)
        self.assertIn('test editing', str(results.data))

    def test_deleting_item(self):
        # Test API can delete an existing bucketlist. (DELETE request)
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        res = self.client().post(
            '/bucketlists/1/items', headers=self.valid_token(), data=self.item)
        self.item['name'] = 'test editing'
        res = self.client().delete('/bucketlists/1/items/1', headers=self.valid_token())
        self.assertEqual(res.status_code, 200)
        results = self.client().get(
            '/bucketlists/1/items/1', headers=self.valid_token(), data=self.item)
        self.assertIn('Item not found', str(results.data))

    def test_search_non_existent_bucketlist(self):
        # Test search q  for non existing data
        res = self.client().get(
            '/bucketlists/1/items?q=item5', headers=self.valid_token(), data=self.item)
        self.assertIn('Bucketlist not found', str(res.data))

    def test_search_non_existent_item(self):
        # Test search q  for non existing data
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        res = self.client().get(
            '/bucketlists/1/items?q=item5', headers=self.valid_token(), data=self.item)
        self.assertIn('There are no items added yet.', str(res.data))

    def test_search_limit_works(self):
        # Test search limit
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        res = self.client().post(
            '/bucketlists/1/items', headers=self.valid_token(), data=self.item)
        self.item['name'] = 'test2'
        res = self.client().post(
            '/bucketlists/1/items', headers=self.valid_token(), data=self.item)
        res = self.client().get(
            '/bucketlists/1/items?limit=1', headers=self.valid_token(), data=self.item)
        self.assertEqual(len(json.loads(res.data.decode())['items']), 1)

    def test_search_with_non_numeric(self):
        # Test search limit with no numerical
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        res = self.client().get(
            '/bucketlists/1/items?limit=test', headers=self.valid_token(), data=self.item)
        self.assertIn('Please pass a numeral.', json.loads(res.data.decode()).values())

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
