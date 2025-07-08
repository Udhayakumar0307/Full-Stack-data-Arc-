from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    projects = db.relationship('Project', backref='owner', cascade="all, delete")

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/users', methods=['GET', 'POST'])
def list_users():
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(User(name=name))
        db.session.commit()
        return redirect(url_for('list_users'))
    
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(User(name=name))
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('users.html')

@app.route('/users/delete/<int:id>', methods=['POST'])
def remove_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))

@app.route('/projects/add', methods=['GET', 'POST'])
def add_project():
    users = User.query.all()
    if request.method == 'POST':
        title = request.form['title']
        user_id = request.form['user_id']
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_project = Project(title=title, image=filename, user_id=user_id)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('add_project'))  
    return render_template('projects.html', users=users)

@app.route('/projects/delete/<int:id>', methods=['POST'])
def remove_project(id):
    project = Project.query.get_or_404(id)
    if project.image:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], project.image))
        except FileNotFoundError:
            pass
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
