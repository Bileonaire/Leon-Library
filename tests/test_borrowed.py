"""Test the borrowed books endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
from .base_test import BaseTests


class BorrowedBookTests(BaseTests):
    """Tests functionality of the meal endpoint"""

    def test_admin_get_all(self):
        """Tests admin successfully getting all borrowed book"""
        borrowed_books = self.app.get( # pylint: disable=W0612
            '/api/v1/borrowed',
            headers=self.admin_header)
        response = borrowed_books
        self.assertEqual(response.status_code, 200)


    def test_admin_get_one(self):
        """Tests admin successfully getting a book"""
        data = json.dumps({"borrowed_book" : "book of legends", "author" : "bileonaire"})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v1/borrowed', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.get('/api/v1/borrowed/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_one(self):
        """Tests user successfully getting a book"""
        data = json.dumps({"borrowed_book" : "book of legends", "author" : "bileonaire"})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v1/borrowed', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.get('/api/v1/borrowed/1', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing(self):
        """Test getting a book while providing non-existing id"""
        response = self.app.get('/api/v1/borrowed/10', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_book_update(self):
        """Test a successful book update"""
        # initial_data = json.dumps({"borrowed_book" : "book of legends", "author" : "bileonaire"})
        # added_book = self.app.post( # pylint: disable=W0612
        #     '/api/v1/borrowed', data=initial_data,
        #     content_type='application/json',
        #     headers=self.admin_header)
        data = json.dumps({"borrowed_book" : "book of legends", "author" : "bileon", "returned" : True})
        response = self.app.put(
            '/api/v1/borrowed/1', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_update_non_existing(self):
        """Test updating non_existing book"""
        data = json.dumps({"borrowed_book" : "book of legends", "author" : "leon", "returned" : True})
        response = self.app.put(
            '/api/v1/borrowed/12', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_good_deletion(self):
        """Test a successful book deletion"""
        initial_data = json.dumps({"borrowed_book" : "book of legends", "author" : "bileonaire"})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v1/borrowed', data=initial_data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.delete('/api/v1/borrowed/2', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_deleting_non_existing(self):
        """Test deleting book that does not exist"""
        response = self.app.delete('/api/v1/borrowed/15', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
