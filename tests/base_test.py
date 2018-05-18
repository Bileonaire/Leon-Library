"""Authenticate a user and an admin to be used during testing
Set up required items to be used during testing
"""
# pylint: disable=W0612
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
import models


class BaseTests(unittest.TestCase):
    """Authenticate a user and an admin and make the tokens available. Create a meal and menu option"""


    def setUp(self):
        """Authenticate a user and an admin and make the tokens available"""
        self.application = app.create_app('config.TestingConfig')
        user_reg = json.dumps({
            "username" : "user",
            "email" : "user@gmail.com",
            "password" : "12345678",
            "confirm_password" : "12345678"})

        admin_reg = json.dumps({
            "username" : "admin123",
            "email" : "admin123@gmail.com",
            "password" : "123456789",
            "confirm_password" : "123456789",
            "admin" : True})

        self.user_log = json.dumps({
            "email" : "user@gmail.com",
            "password" : "12345678"})

        self.admin_log = json.dumps({
            "email" : "admin123@gmail.com",
            "password" : "123456789"})

        self.app = self.application.test_client()

        
        register_user = self.app.post(
            '/api/v1/auth/register', data=user_reg,
            content_type='application/json')
        register_admin = self.app.post(
            '/api/v1/auth/register', data=admin_reg,
            content_type='application/json')
            
        admin_result = self.app.post(
            '/api/v1/auth/login', data=self.admin_log,
            content_type='application/json')
        
        admin_response = json.loads(admin_result.get_data(as_text=True))
        admin_token = admin_response["token"]
        self.admin_header = {"Content-Type" : "application/json", "x-access-token" : admin_token}
        
        user_result = self.app.post(
            '/api/v1/auth/login', data=self.user_log,
            content_type='application/json')

        user_response = json.loads(user_result.get_data(as_text=True))
        user_token = user_response["token"]
        self.user_header = {"Content-Type" : "application/json", "x-access-token" : user_token}


        book = json.dumps({"book" : "kitabu cha leo", "author" : "leon"})
        borrowed = json.dumps({"borrowed_book" : "kitabu cha leo", "author" : "leon"})
        create_book = self.app.post(
            '/api/v1/books', data=book, content_type='application/json',
            headers=self.admin_header)
        borrow_book = self.app.post(
            '/api/v1/borrowed', data=borrowed, content_type='application/json',
            headers=self.user_header)
