from argparse import _CountAction
from asyncio import constants
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
    
    
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    contenu = db.Column(db.String(100))
    

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age=db.Column(db.Integer)
    job=db.Column(db.String(100))
    marital=db.Column(db.String(100))
    default=db.Column(db.String(100))
    housing=db.Column(db.String(100))
    contact=db.Column(db.String(100))
    month=db.Column(db.String(100))
    day=db.Column(db.String(100))
    education=db.Column(db.String(100))
    loan=db.Column(db.String(100))



