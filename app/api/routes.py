from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    title = request.json['title']
    author = request.json['author']
    length = request.json['length']
    cover = request.json['cover']
    copyright = request.json['copyright']
    description = request.json['description']
    user_token = current_user_token.token
    
    
    book = Book(isbn, title, author, length, cover, copyright, description, user_token = user_token)    
    
    db.session.add(book)
    db.session.commit()
    
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required 
def get_books(current_user_token):
    user_token = current_user_token.token
    books = Book.query.filter_by(user_token = user_token).all()
    response = books_schema.dump(books)
    return jsonify(response)
    
    
@api.route('/books/<id>', methods=['GET'])
@token_required
def get_book(current_user_token, id):
    paper = current_user_token.token
    if paper == current_user_token.token:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify(response)



@api.route('/books/<id>', methods=['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    
    isbn = request.json['isbn']
    title = request.json['title']
    author = request.json['author']
    length = request.json['length']
    cover = request.json['cover']
    copyright = request.json['copyright']
    description = request.json['description']
    user_token = current_user_token.token
    
    book.isbn = isbn
    book.title = title
    book.author = author
    book.length = length
    book.cover = cover
    book.copyright = copyright
    book.description = description
    book.user_token = current_user_token.token
    
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods=['DELETE'])
@token_required
def delete(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)