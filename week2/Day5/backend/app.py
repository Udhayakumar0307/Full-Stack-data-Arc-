from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

users = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data.get('email', '')

    if username in users:
        return jsonify({'error': 'User already exists'}), 409

    users[username] = {
        'password': generate_password_hash(password),
        'email': email,
        'file': None
    }
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = users.get(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'}), 200

@app.route('/upload/<username>', methods=['POST'])
def upload(username):
    if username not in users:
        return jsonify({'error': 'User does not exist'}), 404

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    filename = f"{username}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    users[username]['file'] = filename
    return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/users', methods=['GET'])
def view_users():
    return jsonify([
        {'username': u, 'email': users[u]['email'], 'file': users[u]['file']}
        for u in users
    ])

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/delete/<username>', methods=['DELETE'])
def delete_user(username):
    if username in users:
        file = users[username]['file']
        if file:
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, file))
            except FileNotFoundError:
                pass
        del users[username]
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
