import os
import unittest
import json
from app import create_app, db
from app.models.models import User


class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'username': 'Test text', 'email': 'Test@text.com', 'password': 'Testtext'}

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()
            # test_user = User('test', 'test@mail.com')
            # test_user.hash_password('test')
            # db.session.add(test_user)
            # db.session.commit()

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


# class BucketlistTestCase(unittest.TestCase):
#     """This class represents the bucketlist test case"""

#     def setUp(self):
#         """Define test variables and initialize app."""
#         self.app = create_app(config_name="testing")
#         self.client = self.app.test_client
#         self.user = {'name': 'Test text'}

#         # binds the app to the current context
#         with self.app.app_context():
#             db.create_all()

#     def test_bucketlist_creation(self):
#         """Test API can create a bucketlist (POST request)"""
#         res = self.client().post('/bucketlists/', data=self.bucketlist)
#         self.assertEqual(res.status_code, 201)
#         self.assertIn('This is random text', str(res.data))

#     def test_api_can_get_all_bucketlists(self):
#         """Test API can get a bucketlist (GET request)."""
#         res = self.client().post('/bucketlists/', data=self.bucketlist)
#         self.assertEqual(res.status_code, 201)
#         res = self.client().get('/bucketlists/')
#         self.assertEqual(res.status_code, 200)
#         self.assertIn('This is random text', str(res.data))

#     def test_api_can_get_bucketlist_by_id(self):
#         """Test API can get a single bucketlist by using it's id."""
#         rv = self.client().post('/bucketlists/', data=self.bucketlist)
#         self.assertEqual(rv.status_code, 201)
#         result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
#         result = self.client().get(
#             '/bucketlists/{}'.format(result_in_json['id']))
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('This is random text', str(result.data))

#     def test_bucketlist_can_be_edited(self):
#         """Test API can edit an existing bucketlist. (PUT request)"""
#         rv = self.client().post(
#             '/bucketlists/',
#             data={'name': 'Eat, pray and love'})
#         self.assertEqual(rv.status_code, 201)
#         rv = self.client().put(
#             '/bucketlists/1',
#             data={
#                 "name": "Dont just eat, but also pray and love :-)"
#             })
#         self.assertEqual(rv.status_code, 200)
#         results = self.client().get('/bucketlists/1')
#         self.assertIn('Dont just eat', str(results.data))

#     def test_bucketlist_deletion(self):
#         """Test API can delete an existing bucketlist. (DELETE request)."""
#         rv = self.client().post(
#             '/bucketlists/',
#             data={'name': 'Eat, pray and love'})
#         self.assertEqual(rv.status_code, 201)
#         res = self.client().delete('/bucketlists/1')
#         self.assertEqual(res.status_code, 200)
#         # Test to see if it exists, should return a 404
#         result = self.client().get('/bucketlists/1')
#         self.assertEqual(result.status_code, 404)

#     def tearDown(self):
#         """teardown all initialized variables."""
#         with self.app.app_context():
#             # drop all tables
#             db.session.remove()
#             db.drop_all()


# class ItemTestCase(unittest.TestCase):
#     """This class represents the item test case"""

#     def setUp(self):
#         """Define test variables and initialize app."""
#         self.app = create_app(config_name="testing")
#         self.client = self.app.test_client
#         self.bucketlist = {'name': 'This is random text'}

#         # binds the app to the current context
#         with self.app.app_context():
#             db.create_all()

#     def test_item_creation(self):
#         """Test API can create a item (POST request)"""
#         res = self.client().post('/bucketlists/1/items/', data=self.bucketlist)
#         self.assertEqual(res.status_code, 201)
#         self.assertIn('This is random text', str(res.data))

#     def test_item_can_be_edited(self):
#         """Test API can edit an existing bucketlist. (PUT request)"""
#         rv = self.client().post(
#             '/bucketlists/',
#             data={'name': 'Eat, pray and love'})
#         self.assertEqual(rv.status_code, 201)
#         rv = self.client().post(
#             '/bucketlists/1/items/',
#             data={'name': 'Eat, pray and love'})
#         self.assertEqual(rv.status_code, 201)
#         rv = self.client().put(
#             '/bucketlists/1/items/1',
#             data={
#                 "name": "Dont just eat, but also pray and love :-)"
#             })
#         self.assertEqual(rv.status_code, 200)
#         results = self.client().get('/bucketlists/1')
#         self.assertIn('Dont just eat', str(results.data))

#     def test_item_deletion(self):
#         """Test API can delete an existing bucketlist. (DELETE request)."""
#         rv = self.client().post(
#             '/bucketlists/',
#             data={'name': 'Eat, pray and love'})
#         self.assertEqual(rv.status_code, 201)
#         rv = self.client().post(
#             '/bucketlists/1/items/',
#             data={'name': 'Eat, pray and love'})
#         self.assertEqual(rv.status_code, 201)
#         res = self.client().delete('/bucketlists/1/items/1')
#         self.assertEqual(res.status_code, 200)
#         # Test to see if it exists, should return a 404
#         result = self.client().get('/bucketlists/1/items/1')
#         self.assertEqual(result.status_code, 404)

#     def tearDown(self):
#         """teardown all initialized variables."""
#         with self.app.app_context():
#             # drop all tables
#             db.session.remove()
#             db.drop_all()

# # Make the tests conveniently executable
# if __name__ == "__main__":
#     unittest.main()
