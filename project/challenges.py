from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
import json
challenges = Blueprint('challenges', __name__)

@challenges.route('/get_challenges')
@login_required
def get_challenges():
    pass #place holder