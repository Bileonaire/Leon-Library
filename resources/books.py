"""Contains all endpoints to manipulate meal information
"""
import datetime

from flask import jsonify, Blueprint, make_response
from flask_restful import Resource, Api, reqparse, inputs

import models
from .auth import token_required, admin_required


class BookList(Resource):
    """Contains GET and POST methods"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'book',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a book',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'author',
            required=False,
            type=str,
            help="kindly provide a valid author's name",
            default="author",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'available',
            required=False,
            nullable=True,
            default=True,
            type=bool,
            location=['form', 'json'])
        super().__init__()
    
    @admin_required
    def post(self):
        """Adds a new book"""
        kwargs = self.reqparse.parse_args()
        for book_id in models.all_books:
            if models.all_books.get(book_id)["book"] == kwargs.get('book'):
                return jsonify({"message" : "book with that name already exists"})

        result = models.Book.create_book(**kwargs)
        return make_response(jsonify(result), 201)

    def get(self):
        """Gets all books"""
        return make_response(jsonify(models.all_books), 200)


class Book(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single book"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'book',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a book name',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'author',
            required=False,
            type=str,
            default="author",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'available',
            required=False,
            nullable=True,
            default=True,
            type=bool,
            location=['form', 'json'])
        
        super().__init__()
    

    def get(self, book_id):
        """Get a particular book"""
        try:
            book = models.all_books[book_id]
            return make_response(jsonify(book), 200)
        except KeyError:
            return make_response(jsonify({"message" : "book does not exist"}), 404)

    @admin_required
    def put(self, book_id):
        """Update a particular book"""
        kwargs = self.reqparse.parse_args()
        result = models.Book.update_book(book_id, **kwargs)
        if result != {"message" : "book does not exist"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)
    
    @admin_required
    def delete(self, book_id):
        """Delete a particular book"""
        result = models.Book.delete_book(book_id)
        if result != {"message" : "the book does not exist"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)

class BorrowedList(Resource):
    """Contains GET and POST methods for manipulating borrowed books data"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'borrowed_book',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a book to borrow',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'author',
            required=False,
            type=str,
            default="author",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'returned',
            required=False,
            nullable=True,
            default=False,
            type=bool,
            location=['form', 'json'])
        super().__init__()
    
    @token_required
    def post(self):
        """Adds a book to the borrowerd books"""
        kwargs = self.reqparse.parse_args()
        for borrowed_id in models.all_borrowed:
            if models.all_borrowed.get(borrowed_id)["borrowed_book"] == kwargs.get('borrowed_book'):
                return jsonify({"message" : "borrowed book with that name already exists"})

        result = models.Borrowed.borrow_book(**kwargs)
        return make_response(jsonify(result), 201)


    def get(self):
        """Gets all borrowed books"""
        return make_response(jsonify(models.all_borrowed), 200)


class Borrowed_book(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single borrowed book"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'borrowed_book',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a book to borrow',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'author',
            required=False,
            type=str,
            default="author",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'returned',
            required=False,
            nullable=True,
            default=False,
            type=bool,
            location=['form', 'json'])
        super().__init__()

    @token_required
    def get(self, borrowed_id):
        """Get a particular borrowed book"""
        try:
            book = models.all_borrowed[borrowed_id]
            return make_response(jsonify(book), 200)
        except KeyError:
            return make_response(jsonify({"message" : "specified borrowed book does not exist"}), 404)

    @admin_required
    def put(self, borrowed_id):
        """Update a particular borrowed book"""
        kwargs = self.reqparse.parse_args()
        result = models.Borrowed.update_borrowed(borrowed_id, **kwargs)
        if result != {"message" : "the specified borrowed book does not exist in borrowed books"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 400)

    @admin_required
    def delete(self, borrowed_id):
        """Delete a particular borrowed book"""
        result = models.Borrowed.delete_book(borrowed_id)
        if result != {"message" : "the specified borrowed book does not exist in borrowed books"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)


books_api = Blueprint('resources.books', __name__)
api = Api(books_api) # create the API
api.add_resource(BookList, '/books', endpoint='books')
api.add_resource(Book, '/books/<int:book_id>', endpoint='book')

api.add_resource(BorrowedList, '/borrowed', endpoint='borrowed')
api.add_resource(Borrowed_book, '/borrowed/<int:borrowed_id>', endpoint='borrowedbook')
