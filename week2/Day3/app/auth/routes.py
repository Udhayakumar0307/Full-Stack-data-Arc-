from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import user_store

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from app.models import user_store

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
     
        user_store.append({'email': email, 'username': username, 'password': password, 'projects': []})

        session['user'] = username 
        return redirect(url_for('auth.dashboard'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in user_store if u['username'] == username and u['password'] == password), None)
        if user:
            session['user'] = username
            return redirect(url_for('auth.dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@auth_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    user = next((u for u in user_store if u['username'] == session['user']), None)
    return render_template('dashboard.html', user=user)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))