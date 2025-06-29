from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("blog.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
init_db()

@app.route('/')
def index():
    with sqlite3.connect("blog.db") as conn:
        posts = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    return render_template("index.html", posts=posts)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with sqlite3.connect("blog.db") as conn:
            conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        return redirect(url_for('index'))
    return render_template("new.html")

@app.route('/post/<int:post_id>')
def post(post_id):
    with sqlite3.connect("blog.db") as conn:
        post = conn.execute("SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()
    if post:
        return render_template("post.html", post=post)
    return "Post not found", 404

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    with sqlite3.connect("blog.db") as conn:
        post = conn.execute("SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()

    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        with sqlite3.connect("blog.db") as conn:
            conn.execute("UPDATE posts SET title=?, content=? WHERE id=?", (new_title, new_content, post_id))
        return redirect(url_for('post', post_id=post_id))

    return render_template("edit.html", post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with sqlite3.connect("blog.db") as conn:
        conn.execute("DELETE FROM posts WHERE id=?", (post_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
