"""Test the book endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
from .base_test import BaseTests


class MealTests(BaseTests):
    """Tests functionality of the meal endpoint"""


    def test_admin_get_one(self):
        """Tests admin successfully getting a book"""
        data = json.dumps({"book" : "book of legends", "author" : "bileonaire"})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v1/books', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.get('/api/v1/books/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_one(self):
        """Tests user successfully getting a book"""
        data = json.dumps({"book" : "book of legends", "author" : "bileonaire"})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v1/books', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.get('/api/v1/books/2', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing(self):
        """Test getting a book while providing non-existing id"""
        response = self.app.get('/api/v1/books/10', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_book_update(self):
        """Test a successful book update"""
        initial_data = json.dumps({"book" : "book of legends", "author" : "bileonaire"})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v1/books', data=initial_data,
            content_type='application/json',
            headers=self.admin_header)
        data = json.dumps({"book" : "book of legends", "author" : "bileon"})
        response = self.app.put(
            '/api/v1/books/1', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_update_non_existing(self):
        """Test updating non_existing book"""
        data = json.dumps({"book" : "book of legends", "author" : "leon"})
        response = self.app.put(
            '/api/v1/books/12', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_deletion(self):
        """Test a successful book deletion"""
        initial_data = json.dumps({"book" : "book of legends", "author" : "bileonaire"})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v1/books', data=initial_data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.delete('/api/v1/books/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_deleting_non_existing(self):
        """Test deleting book that does not exist"""
        response = self.app.delete('/api/v1/books/15', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
