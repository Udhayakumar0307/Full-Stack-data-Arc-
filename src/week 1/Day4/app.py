from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime

app = Flask(__name__)

data_store = []

@app.route('/')
def data_form():
    return render_template('index.html')  

@app.route('/submit', methods=['POST'])
def submit_data():
    title = request.form.get('title')
    author = request.form.get('authory') 
    content = request.form.get('content')

    print(f"DEBUG - title: {title}, author: {author}, content: {content}")

    with open('data.txt', 'a') as f:
        f.write(f"{datetime.datetime.now()}\ntitle: {title}\nauthory: {author}\nMessage: {content}\n\n")

    new_entry = {
        'id': len(data_store) + 1,
        'title': title,
        'authory': author,
        'content': content,
    }
    data_store.append(new_entry)

    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return "<h2>Thank you for your submission!</h2><a href='/'>Go back</a>"

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data_store), 200

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'authory', 'content')):
        return jsonify({'error': 'Invalid data, expected title, authory, and content'}), 400

    new_entry = {
        'id': len(data_store) + 1,
        'title': data['title'],
        'authory': data['authory'],
        'content': data['content'],
    }
    data_store.append(new_entry)

    return jsonify({'message': 'Data added successfully', 'data': new_entry}), 201

if __name__ == '__main__':
    app.run(debug=True)
