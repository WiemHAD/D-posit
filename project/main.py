from unicodedata import name
from flask import Blueprint, redirect, render_template, request, url_for

from flask_login import login_required, current_user

from project.models import User

from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
@main.route('/affiche')
def affiche():
    users = User.query.all()
    return render_template('affiche.html',users=users)

@main.route('/profile')
@login_required
def profile():
    
    return render_template('profile.html')


