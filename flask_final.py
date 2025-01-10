import sqlite3
from flask import Flask, render_template, url_for, request, redirect, session
from cachelib import FileSystemCache
from datetime import timedelta
from flask_session import Session

app = Flask(__name__)
con = sqlite3.connect("data.db", check_same_thread=False)
secret_key = '1234'
cursor = con.cursor()
app.config['SESSION_TYPE']= 'cachelib'
app.config['SESSION_CACHELIB'] = FileSystemCache(cache_dir='flask_session', threshold=500)
Session(app)
@app.route('/add/')
def add():
    return render_template('add.html')


@app.route('/upload/', methods=['POST'])
def save_post():
    description = request.form['description']
    title = request.form['title']
    image = request.files.get('image')
    file_dir = f'static/uploads/{image.filename}'
    image.save(file_dir)
    cursor.execute("INSERT INTO posts (title, description, file_name) VALUES (?,?,?)",(title, description, file_dir))
    con.commit()

    return redirect(url_for('main_page'))


@app.route('/')
def all_posts():
  cursor.execute('SELECT * FROM posts')
  data = cursor.fetchall()
  return render_template('all_post.html', posts= data)

@app.route('/register/', methods=['POST','GET'])
def register():
    return render_template('register.html')
@app.route('/login/')
def login_page():
    return render_template('login.html')
@app.route('/main_page/')
def main_page():
    return render_template('main_page.html')
@app.route('/save_register/', methods=['POST'])
def save_register():

    last_name = request.form['last_name']
    name = request.form['name']
    patronymic = request.form['patronymic']
    gender = request.form['gender']
    email = request.form['email']
    login = request.form['username']
    password = request.form['password']
    cursor.execute('INSERT INTO save_register ( last_name, name, patronymic, gender, email, user_name, password) VALUES(?,?,?,?,?,?,?)',[ last_name, name, patronymic, gender, email, login, password])
    con.commit()
    return redirect(url_for('login_page'))



@app.route('/authorization/',methods=['POST'])
def authorization():

    user_name = request.form['username']
    password = request.form['password']
    cursor.execute('SELECT user_name, password FROM save_register WHERE user_name=(?) and password=(?)', [user_name, password])
    data = cursor.fetchall()
    if user_name ==data and password==data:

        session['login'] = True
        session['user_name'] = user_name
        session.permanent = False
        app.permanent_session_lifetime = timedelta(days=14)
        session.modified = True
        return redirect(url_for('main_page'))
    else:
        return redirect(url_for('login_page'))




app.run(debug=True)
