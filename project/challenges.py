from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, stream_with_context
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
import json
import os
from pathlib import Path

challenges = Blueprint('challenges', __name__)
cwd = os.getcwd()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

flags = {}
file = "project/data/flags.json"
if cwd.endswith('project'):
    file = os.path.join(cwd, 'data', 'flags.json')
    
with open(file, 'r') as f:
    flags = json.load(f)
    flags = flags["flags"]
    f.close()

@challenges.route('/get_challenges', methods=['GET'])
@login_required
def get_challenges():
    file_path = "project/data/challData.json"
    if cwd.endswith('project'):
        file_path = os.path.join(cwd, 'data', 'challData.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
        f.close()
    return Response(response=json.dumps(data), status=200, mimetype='application/json')

@challenges.route('/submit_challenge', methods=['POST'])
@login_required
def submit_challenge():
    data = request.form
    user_id = current_user.id
    user_flag = data.get('flag')
    chall_id = data.get('challenge_id')
    
    if not user_flag or not chall_id:
        return Response(response=json.dumps({"error": "Missing flag or challenge_id"}), status=400, mimetype='application/x-www-form-urlencoded')
    print(f"User {user_id} submitted flag: {user_flag} for challenge {chall_id}")
    for flag in flags:
        if flag['id'] == int(chall_id):
            if flag['flag'] == user_flag:
                finished_challenges = list(current_user.completed_challenges or [])
                print(finished_challenges)
                finished_challenges.append(int(chall_id))
                current_user.completed_challenges = finished_challenges
                print(current_user.completed_challenges)
                db.session.commit()
                return Response(response=json.dumps({"success": "Flag is correct"}), status=200, mimetype='application/x-www-form-urlencoded')
            else:
                print("Invalid flag")
                return Response(response=json.dumps({"error": "Invalid flag"}), status=401, mimetype='application/x-www-form-urlencoded')