from flask import Flask, render_template, request, redirect, session
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        # Add authentication logic here, like checking against users.json
        session['username'] = username
        return redirect('/profile')
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    if not username:
        return redirect('/login')

    # Load user data from users.json, handle image uploads, etc.

    return render_template('user_profile.html', username=username, images=images, paragraphs=paragraphs)

if __name__ == '__main__':
    app.run(debug=True)
