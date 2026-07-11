from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required, current_user
from . import db
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/challs')
@login_required
def challs():
    return render_template('challs.html', completed_challenges=current_user.completed_challenges or [])

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')