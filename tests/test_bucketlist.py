"""
This tests the functions in the bucketlist view
"""


import unittest
import json
from app import create_app, db


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

    def valid_token(self):
        # creating a valid token
        self.client().post('/auth/register', data=self.user)
        user = self.client().post('/auth/login', data=self.user)
        token = json.loads(user.data.decode())['token']
        return {'Authorization': token}

    def test_get_empty_bucketlist_with_valid_token(self):
        # Test getting empty bucketlist from db
        res = self.client().get('/bucketlists', headers=self.valid_token())
        self.assertEqual(res.status_code, 200)
        self.assertIn(len(json.loads(res.data.decode())['bucketlist']), 0)

    def test_bucketlist_creation(self):
        # Test with valid token
        res = self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('test bucketlist', str(json.loads(res.data.decode())['name']))

    def test_bucketlist_creation_with_missing_data(self):
        # Test with missing data
        self.bucketlist['name'] = ''
        res = self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        self.assertEqual(res.status_code, 403)
        self.assertIn('Some data is missing!', str(res.data))

    def test_getting_bucketlist_from_db(self):
        # Test getting bucketlist from db
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        res = self.client().get('/bucketlists', headers=self.valid_token())
        self.assertEqual(res.status_code, 200)
        self.assertIn('test bucketlist', str(res.data))

    def test_searching_bucketlist(self):
        # Test search q
        self.bucketlist['name'] = 'bucket2'
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        res = self.client().get('/bucketlists?q=bucket2', headers=self.valid_token())
        self.assertIn('bucket2', str(res.data))
        res = self.client().get('/bucketlists?q=buck', headers=self.valid_token())
        self.assertEqual(len(json.loads(res.data.decode())['bucketlist']), 1)

    def test_searching_bucketlist_non_existance(self):
        # Test search q  for non existing data
        res = self.client().get(
            '/bucketlists?q=bucket5', headers=self.valid_token(), data=self.bucketlist)
        self.assertEqual(len(json.loads(res.data.decode())['bucketlist']), 0)

    def test_getting_buckets_with_limit(self):
        # Test search limit
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        self.bucketlist['name'] = 'name2'
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        res = self.client().get(
            '/bucketlists?limit=1', headers=self.valid_token(), data=self.bucketlist)
        self.assertEqual(len(json.loads(res.data.decode())['bucketlist']), 1)

    def test_limit_with_non_numeral(self):
        # Test search limit with no numerical
        res = self.client().get(
            '/bucketlists?limit=test', headers=self.valid_token(), data=self.bucketlist)
        self.assertIn('Please pass a numeral.', json.loads(res.data.decode()).values())


    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        res = self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        id = json.loads(res.data.decode())['id']
        result = self.client().get(
            '/bucketlists/{}'.format(id), headers=self.valid_token(), data=self.bucketlist)
        self.assertEqual(result.status_code, 200)
        self.assertIn('test bucketlist', str(result.data))

    def test_editing_a_bucketlist(self):
        # Test API can edit an existing bucketlist. (PUT request)
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        self.bucketlist['name'] = 'new name'
        res = self.client().put(
            '/bucketlists/1', headers=self.valid_token(), data=self.bucketlist)
        self.assertEqual(res.status_code, 200)
        results = self.client().get(
            '/bucketlists/1', headers=self.valid_token(), data=self.bucketlist)
        self.assertIn('new name', str(results.data))

    def test_delete_bucketlist(self):
        # Test API can delete an existing bucketlist. (DELETE request)
        self.client().post('/bucketlists', headers=self.valid_token(), data=self.bucketlist)
        res = self.client().delete(
            '/bucketlists/1', headers=self.valid_token(), data=self.bucketlist)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/bucketlists/1', headers=self.valid_token(), data=self.bucketlist)
        self.assertEqual(result.status_code, 403)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
