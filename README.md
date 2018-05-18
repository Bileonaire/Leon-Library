[![Build Status](https://travis-ci.org/Bileonaire/Leon-Library.svg?branch=Develop-API-version1)](https://travis-ci.org/Bileonaire/Leon-Library)
[![Coverage Status](https://coveralls.io/repos/github/Bileonaire/Leon-Library/badge.svg)](https://coveralls.io/github/Bileonaire/Leon-Library)

# Leon-Library
Leon Library allows the librarian to run the library and users to borrow and return books

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Git
* Python 3.6.4
* Virtualenv

### Quick Start

1. Clone the repository

```
$ git clone https://github.com/Bileonaire/Leon-Library.git
$ cd into the created folder
```
  
2. Initialize and activate a virtualenv

```
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

3. Install the dependencies

```
$ pip install -r requirements.txt
```

4. Initialize environment variables

```
$ export SECRET_KEY=<SECRET KEY>
```

5. Run the development server

```
$ python app.py
```

6. Navigate to [http://localhost:5000](http://localhost:5000)

At the / endpoint you should see Welcome to library books API displayed in your browser.

## Endpoints

Here is a list of all endpoints in the Library API

Endpoint | Functionality 
------------ | -------------
POST   /api/v1/auth/signup | Register a user
POST   /api/v1/auth/login | Log in user
POST   /api/v1/users | Create a user
GET    /api/v1/users | Get all users
GET   /api/v1/users/id | Get a single user
PUT  /api/v1/users/id | Update a single user
DELETE   /api/v1/users/id | Delete a single user
POST   /api/v1/books | Create new book
GET   /api/v1/books | Get all books
GET   /api/v1/books/id | Get a single book
PUT   /api/v1/books/id | Update a single book
DELETE   /api/v1/books/id | Delete a single book
POST   /api/v1/borrowed | Create new borrowed book
GET   /api/v1/borrowed | Get all borrowed books
DELETE   /api/v1/borrowed/id | Delete a single borrowed book
GET   /api/v1/borrowed/id | Get a single borrowed book

## Running the tests

To run the automated tests simply run

```
nosetests tests
```

### And coding style tests

Coding styles tests are tests that ensure conformity to coding style guides. In our case, they test conformity to
PEP 8 style guides

```
pylint app.py
```

## Deployment

Ensure you use Productionconfig settings which have DEBUG set to False

## Built With

* HTML5
* CSS3
* Python 3.6.4
* Flask - The web framework used

## GitHub pages

https://Bileonaire.github.io/

## Heroku

https://.herokuapp.com/apidocs

## Versioning

Most recent version is version 1

## Authors

Leon Kioko.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration and encouragement
* etc
