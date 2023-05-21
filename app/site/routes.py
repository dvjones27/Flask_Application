from flask import Blueprint, request, jsonify, render_template, redirect, flash, url_for
from flask_login import current_user, login_required
from helpers import token_required
from models import db, User, Book, book_schema, books_schema
import requests 

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@site.route('/books')
@login_required
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@site.route('/create_book', methods=['POST'])
def create_book():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    length = request.form['length']
    cover = request.form['cover']
    copyright = request.form['copyright']
    description = request.form['description']
    user_token = current_user.token
    
    book = Book(isbn, title, author, length, cover, copyright, description, user_token = user_token)
    
    db.session.add(book)
    db.session.commit()
    
    return redirect(url_for('site.books'))


@site.route('/search')
def search():

    return render_template('search.html')


# @site.route('/<int:id>/update', methods=['GET','PUT', 'POST'])
# def update(id):
#     # isbn = current_user.isbn
#     # book = Book.query.get(isbn)
    
    
#     user_id = current_user.id
#     book = Book.query.filter_by(user_id=user_id).first()
    
#     if request.method == 'PUT':
#         isbn = request.form['isbn']
#         title = request.form['title']
#         author = request.form['author']
#         length = request.form['length']
#         cover = request.form['cover']
#         copyright = request.form['copyright']
#         description = request.form['description']
        
        
#         book.isbn = isbn
#         book.title = title
#         book.author = author
#         book.length = length
#         book.cover = cover
#         book.copyright = copyright
#         book.description = description
        
#         db.session.add(book)
#         db.session.commit()
        
#         return redirect(url_for('site.books'))
    
    
#     return redirect(url_for('site.books'))
    
    # book = Book.query.get_or_404(isbn)
    # if not request.form:
    #     abort(404)
        
    # book = Book.query.get(isbn)
    # if book is None:
    #     abort(404)
        
    # book.isbn = request.form.get('isbn', book.isbn)
    # book.title = request.form.get('title', book.title)
    # book.author = request.form.get('author', book.author)
    # book.length = request.form.get('length', book.length)
    # # book.cover = request.form.get('cover', book.cover)
    # book.copyright = request.form.get('copyright', book.copyright)
    # book.description = request.form.get('description', book.description)
    # db.session.commit()
    # return redirect(url_for('site.books'))

# ('/<int:id>/update', methods=['GET','POST'])
# def update(id):
#     user_id = current_user.id
#     book = Book.query.filter_by(user_id=user_id).first()

#     return redirect(url_for('site.update', book = book))


@site.route('/update/<string:isbn>', methods=[ 'GET','POST'])
@login_required
def update(isbn):
    # i = Book.query.get_or_404(id)
    # book = Book.query.get(id)
    # if 'isbn' in request.form:
    #     i.isbn = request.form['isbn']
    # db.session.commit()
    
    
    # user_id = current_user.id
    # book = Book.query.filter_by(isbn=isbn).first()
    book = Book.query.filter_by(isbn=isbn).first()
    # form = BookForm(obj=book)
    if request.method == 'POST':
        # db.session.delete(book)
        # db.session.commit()
        if book:
            isbn = request.form['isbn']
            title = request.form['title']
            author = request.form['author']
            length = request.form['length']
            cover = request.form['cover']
            copyright = request.form['copyright']
            description = request.form['description']
        
        # book.isbn = isbn
        # book.title = title
        # book.author = author
        # book.length = length
        # book.cover = cover
        # book.copyright = copyright
        # book.description = description
                
            book = Book(
                isbn = isbn,
                title = title,
                author =author,
                length = length,
                cover = cover,
                copyright = copyright,
                description = description
            )
    
            db.session.update(book)
            db.session.commit()
            return redirect(url_for('site.books'))
        return f"There is no book with isbn: {isbn}."
        
    return redirect(url_for('site.books'))


# return redirect(url_for('site.books'))

# @site.route ('/<int:isbn>/update', methods= ['PUT'])
# def update(isbn):
#     if not request.form:
#         abort(400)
#     book = Book.query.get(isbn)
#     if book is None:
#         abort(404)
#     book.isbn = request.form.get('isbn', book.isbn)
#     book.title = request.form.get('title', book.title)
#     book.author = request.form.get('author', book.author)
#     book.length = request.form.get('length', book.length)
#     book.cover = request.form.get('cover', book.cover)
#     book.copyright = request.form.get('copyright', book.copyright)
#     book.description = request.form.get('description', book.description)
#     db.session.commit()
#     return redirect(url_for('site.books'))



@site.route('/', methods=[' GET'])
def retrieveBookList():
    books = Book.query.all()
    return render_template('index.html', books = books)



@site.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    books = Book.query.get(id)
    if request.method == 'POST':
        if books:
            db.session.delete(books)
            db.session.commit()
            return redirect(url_for('site.books'))
        abort(404)
    return render_template('site.books')
    