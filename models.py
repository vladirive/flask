from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime
db = SQLAlchemy()

class User(db.Model):    
    __tablename__ = 'users' #para asiganar un nombre de la tabla diferente, ya que por defecto asume como nombre el que lleva la clase
    id = db.Column(db.Integer, primary_key=True)
    coments = db.relationship('Coment')
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))
    created_date = db.Column(db.DateTime, default = datetime.datetime.now)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self._create_password(password)

    def _create_password(self, password):
        return generate_password_hash(password, method='sha256')

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class Coment(db.Model):
    __tablename__ = 'coments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text())
    created_date = db.Column(db.DateTime, default = datetime.datetime.now) 
