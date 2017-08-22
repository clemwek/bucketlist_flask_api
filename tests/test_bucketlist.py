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

    def test_bucketlist_creation_and_getting(self):
        """Test API can create a bucketlist (POST request)"""
        res = self.client().post('/bucketlists', data=self.bucketlist)
        self.assertEqual(res.status_code, 401)
        self.assertIn('token is missing!', str(res.data))

        # reating a valid token
        self.client().post('/auth/register', data=self.user)
        user = self.client().post('/auth/login', data=self.user)
        token = json.loads(user.data.decode())['token']
        token = {'Authorization': token}

        # Test getting empty bucketlist from db
        res = self.client().get('/bucketlists', headers=token)
        self.assertEqual(res.status_code, 403)
        self.assertIn('There are no bucketlists added yet.', str(res.data))

        # Test with valid token
        res = self.client().post('/bucketlists', headers=token, data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('test bucketlist', str(json.loads(res.data.decode())['name']))

        # Test with missing data
        self.bucketlist['name'] = ''
        res = self.client().post('/bucketlists', headers=token, data=self.bucketlist)
        self.assertEqual(res.status_code, 403)
        self.assertIn('Some data is missing!', str(res.data))


        # Test getting bucketlist from db
        res = self.client().get('/bucketlists', headers=token)
        print(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('test bucketlist', str(res.data))

        # Test search q
        self.bucketlist['name'] = 'bucket2'
        res = self.client().post('/bucketlists', headers=token, data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('bucket2', str(json.loads(res.data.decode())['name']))
        res = self.client().get('/bucketlists?q=bucket2', headers=token)
        self.assertIn('bucket2', str(res.data))
        res = self.client().get('/bucketlists?q=buck', headers=token)
        self.assertEqual(len(json.loads(res.data.decode())['bucketlist']), 2)

        # Test search q  for non existing data
        res = self.client().get('/bucketlists?q=bucket5', headers=token, data=self.bucketlist)
        self.assertIn('Bucket not found in the list', str(res.data))

        # Test search limit
        res = self.client().get('/bucketlists?limiit=1', headers=token, data=self.bucketlist)
        print(res.data, 'This is the seae=rch limit')
        self.assertEqual(len(json.loads(res.data.decode())['bucketlist']), 2)

        # Test search limit with no numerical
        res = self.client().get('/bucketlists?limit=test', headers=token, data=self.bucketlist)
        self.assertIn('Please pass a numeral.', json.loads(res.data.decode()).values())


    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        self.client().post('/auth/register', data=self.user)
        user = self.client().post('/auth/login', data=self.user)
        token = json.loads(user.data.decode())['token']
        token = {'Authorization': token}
        res = self.client().post('/bucketlists', headers=token, data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        id = json.loads(res.data.decode())['id']
        result = self.client().get(
            '/bucketlists/{}'.format(id), headers=token, data=self.bucketlist)
        self.assertEqual(result.status_code, 200)
        self.assertIn('test bucketlist', str(result.data))

        # Test API can edit an existing bucketlist. (PUT request)
        self.bucketlist['name'] = 'new name'
        res = self.client().put('/bucketlists/1', headers=token, data=self.bucketlist)
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/bucketlists/1', headers=token, data=self.bucketlist)
        self.assertIn('new name', str(results.data))

        # Test API can delete an existing bucketlist. (DELETE request)
        res = self.client().delete('/bucketlists/1', headers=token, data=self.bucketlist)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/bucketlists/1', headers=token, data=self.bucketlist)
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
