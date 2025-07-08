from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import user_store

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/', methods=['GET', 'POST'])
def project_list():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = next((u for u in user_store if u['username'] == session['user']), None)
    if not user:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        user['projects'].append({'title': title, 'description': desc})
        return redirect(url_for('projects.project_list'))

    return render_template('projects.html', projects=user['projects'])