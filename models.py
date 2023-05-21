from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False, default='')
    last_name = db.Column(db.String(150), nullable = False, default = '')
    username = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    token = db.Column(db.String, default = '', unique = True )
    g_auth_verify = db.Column(db.Boolean, default = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # books = db.relationship('Book', backref = 'user', lazy = True)
    
    def __init__(self, first_name='', last_name='', username='', email='',   password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
        
    def set_token(self, length):
        return secrets.token_hex(length)
    

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database using {self.username}.'
    

class Book(db.Model):
    isbn = db.Column(db.String(15), primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    length = db.Column(db.Integer())
    cover = db.Column(db.String(150))
    copyright = db.Column(db.DateTime(timezone=False))
    description = db.Column(db.String(4500))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    
    def __init__(self, isbn, title, author, length, cover, copyright, description, user_token):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.length = length
        self.cover = cover
        self.copyright = copyright
        self.description = description
        self.user_token = user_token
    
    def __repr__(self):
        return f'The book {self.title} by {self.author} having a copyright date of {self.copyright} was created.'
    
    
class BookSchema(ma.Schema):
    class Meta:
        fields = ['isbn', 'title', 'author', 'length', 'cover', 'copyright', 'description']

book_schema = BookSchema()
books_schema = BookSchema(many=True)