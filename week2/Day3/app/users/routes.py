from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import user_store

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET', 'POST'])
def manage_users():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not any(u['username'] == username for u in user_store):
            user_store.append({'username': username, 'password': password, 'projects': []})
        return redirect(url_for('users.manage_users'))

    return render_template('users.html', members=user_store)