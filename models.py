"""Handles data storage for Users, Meals and Orders
"""

all_users = {}
user_count = 1

all_books = {}
book_count = 1

all_borrowed = {}
borrowed_count = 1

# all_orders = {}
# order_count = 1


class User(object):
    """Contains methods to add, update and delete a user"""


    @staticmethod
    def create_user(username, email, password, admin=False, **kwargs):
        """Creates a new user and appends his information to the all_users dictionary"""
        global all_users
        global user_count
        all_users[user_count] = {"id": user_count, "username" : username,
                                 "email" : email, "password" : password, "admin" : admin}
        new_user = all_users[user_count]
        user_count += 1
        return new_user


    @staticmethod
    def update_user(user_id, username, email, password, admin=False, **kwargs):
        """Updates user information"""
        if user_id in all_users.keys():
            all_users[user_id] = {"id" : user_id, "username" : username, "email" : email,
                                  "password" : password, "admin" : admin}
            return all_users[user_id]
        return {"message" : "user does not exist"}

    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        try:
            del all_users[user_id]
            return {"message" : "user successfully deleted"}
        except KeyError:
            return {"message" : "user does not exist"}


class Book(object):
    """Contains methods to add, update and delete a book"""


    @staticmethod
    def create_book(book, author, availabe=True, **kwargs):
        """Creates a book and appends this information to books dictionary"""
        global all_books
        global book_count
        all_books[book_count] = {"id": book_count, "book" : book, "author": author, "available": True}
        new_book = all_books[book_count]
        book_count += 1
        return new_book

    @staticmethod
    def update_book(book_id, book, author, available, **kwargs):
        """Updates book information"""
        if book_id in all_books.keys():
            all_books[book_id] = {"id": book_id, "book" : book, "author" : author, "available" : available}
            return all_books[book_id]
        return {"message" : "book does not exist"}

    @staticmethod
    def delete_book(book_id):
        """Deletes a book"""
        try:
            del all_books[book_id]
            return {"message" : "the book successfully deleted"}
        except KeyError:
            return {"message" : "the book does not exist"}


class Borrowed(object):
    """Contains methods to add, update and delete borrowed books"""


    @staticmethod
    def borrow_book(borrowed_book, author, returned=False, **kwargs):
        """Creates a new borrowed book and appends this information to the all_borrowed dictionary"""
        global all_borrowed
        global borrowed_count
        all_borrowed[borrowed_count] = {"id": borrowed_count, "borrowed_book" : borrowed_book, "author": author,
                                        "returned": returned}
        new_borrowed_book = all_borrowed[borrowed_count]
        borrowed_count += 1
        return new_borrowed_book

    @staticmethod
    def update_borrowed(borrowed_id, borrowed_book, author, returned=False, **kwargs):
        """Updates book information in all_borrowed dictionary"""
        if borrowed_id in all_borrowed.keys():
            all_borrowed[borrowed_id] = {"id": borrowed_id, "borrowed_book" : borrowed_book, "author" : author}
            return all_borrowed[borrowed_id]
        return {"message" : "the specified borrowed book does not exist in borrowed books"}

    @staticmethod
    def delete_book(borrowed_id):
        """Deletes a borrowed book from the all borrowed dictionary"""
        try:
            del all_borrowed[borrowed_id]
            return {"message" : "borrowed book successfully deleted"}
        except KeyError:
            return {"message" : "the specified borrowed book does not exist in borrowed books"}
