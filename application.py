from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), unique=True, nullable=True)
    author = db.Column(db.String(100), unique=False, nullable=False)
    publisher = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, book_name, author, publisher):
        self.book_name = book_name
        self.author = author
        self.publisher = publisher

    def __repr__(self):
        return f'<Book {self.book_name} by {self.author}, published by {self.publisher}, id: {self.id}>'

@app.route('/')
def hello_world():
    return 'Enter book at the end of the url to see the book details'

@app.route('/books')
def books():
    from application import db, Book
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)
    return {'books': output}

@app.route(f'/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({"id": book.id, "book_name": book.book_name, "author": book.author, "publisher": book.publisher})
    
@app.route('/book', methods=['POST'])
def add_book():
    from application import db, Book
    new_book = Book(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(new_book)
    db.session.commit()
    return 'Book added successfully'

@app.route('/book', methods=['DELETE'])
def delete_book(id):
    from application import db, Book
    book_id = request.json['id']
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return 'Book deleted successfully'
    else:
        return 'Book not found'