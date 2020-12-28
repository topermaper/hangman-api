from app import db,app
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
import json

class User(db.Model):

    __tablename__ = 'tUser'

    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name     = db.Column(db.String(100))
    games    = db.relationship('Game', lazy=True, backref=db.backref('user', lazy=True))

    def verify_password(self,password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "id:{}, email:{}, password:{}, name:{}".format(self.id, self.email, self.password, self.name)