from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'

def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        users = load_users()
        if username in users:
            session['username'] = username
            return redirect('/profile')
        else:
            return 'Username not found'
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    if not username:
        return redirect('/login')

    users = load_users()
    user_data = users.get(username, {'images': [], 'paragraphs': []})

    if request.method == 'POST':
        image = request.files['image']
        paragraph = request.form['paragraph']
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_filename)
        user_data['images'].append(image.filename)
        user_data['paragraphs'].append(paragraph)
        users[username] = user_data
        save_users(users)

    return render_template('user_profile.html', username=username, images=user_data['images'], paragraphs=user_data['paragraphs'])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as file:
            json.dump({}, file)
    app.run(debug=True)
