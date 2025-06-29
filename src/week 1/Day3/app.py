from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

@app.route('/')
def feedback_form():
    thankyou = request.args.get('thankyou')
    return render_template('index.html', thankyou=thankyou)

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    with open('feedback.txt', 'a') as f:
        f.write(f"{datetime.datetime.now()}\nName: {name}\nEmail: {email}\nMessage: {message}\n\n")

    return redirect(url_for('feedback_form', thankyou=1))

if __name__ == '__main__':
    app.run(debug=True)
