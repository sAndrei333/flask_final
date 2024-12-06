import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
con = sqlite3.connect("data.db", check_same_thread=False)
cursor = con.cursor()

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
    cursor.execute("INSERT INTO posts (title, description, file_name) VALUES (?, ?,?)",(title, description, file_dir))
    con.commit()

    return 'ok'


@app.route('/all_post/')
def all_posts():
  cursor.execute('SELECT * FROM posts')
  data = cursor.fetchall()
  return render_template('all_post.html', posts= data)




app.run(debug=True)