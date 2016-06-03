#!/usr/bin/python3
from tornado.testing import AsyncHTTPTestCase
import links
import json
from unittest import mock


class RegisterTestCase(AsyncHTTPTestCase):
    def get_app(self):
        links.settings['debug'] = False
        return links.make_app()

    def test_invalid_registration_data(self):
        response = self.fetch('/api/v1.0/register', method='POST', body='')
        self.assertEqual(response.code, 400)

        response = self.post('register')
        self.assertEqual(response.code, 400)

        response = self.post('register', {'email': ''})
        self.assertEqual(response.code, 400)

        response = self.post('register', {'email': 'invalid'})
        self.assertEqual(response.code, 400)

        response = self.post('register', {'email': 81})
        self.assertEqual(response.code, 400)

        response = self.post('register', {'invalid_field': ''})
        self.assertEqual(response.code, 400)

        response = self.post('register', {'email': 'invalid_email'})
        self.assertEqual(response.code, 400)

    @mock.patch('links.db')
    def test_user_already_exist(self, mock_mongo):
        mock_mongo.users.find_one.return_value = True
        user = {'email': 'test@mail.ru', 'nick':'', 'pswd0': 'qwerasdf', 'pswd1': 'qwerasdf'}
        
        response = self.post('register', user)
        self.assertEqual(response.code, 400)

    @mock.patch('links.db')
    def test_registration(self, mock_mongo):
        mock_mongo.users.find_one.return_value = False
        user = {'email': 'test@mail.ru', 'nick':'', 'pswd0': 'qwerasdf', 'pswd1': 'qwerasdf'}
        
        response = self.post('register', user)
        mock_mongo.users.save.assert_called_once_with(mock.ANY)
        self.assertEqual(response.code, 200)

    @mock.patch('links.db')
    def test_optional_nick(self, mock_mongo):        
        mock_mongo.users.find_one.return_value = False
        def side_effect(user):
            if user['nick'] != user['email']: raise Exception()
        mock_mongo.users.save.side_effect = side_effect
        user = {'email': 'test@mail.ru', 'nick':'', 'pswd0': 'qwerasdf', 'pswd1': 'qwerasdf'}        
        response = self.post('register', user)
        self.assertEqual(response.code, 200)

        del user['nick']
        response = self.post('register', user)
        self.assertEqual(response.code, 200)


    def test_invalid_passwords(self):
        user = {'email': 'test@mail.ru', 'nick':'', 'pswd0': 'first_password', 'pswd1': 'second_password'}
        # test password do not match
        response = self.post('register', user)
        self.assertEqual(response.code, 400)

        user['pswd0'] = 'a'
        user['pswd1'] = 'a'
        # test password too short
        response = self.post('register', user)
        self.assertEqual(response.code, 400)

        user['pswd0'] = 'a'*34
        user['pswd1'] = 'a'*34
        # test password too logn
        response = self.post('register', user)
        self.assertEqual(response.code, 400)


    def post(self, s, data={}):
        return self.fetch('/api/v1.0/{}'.format(s), method='POST', body=json.dumps(data))
    
    # def get(self, s):
    #     return self.fetch('/api/v1.0/{}'.format(s))
