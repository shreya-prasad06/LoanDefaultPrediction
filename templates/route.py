import sqlite3 as sql
from flask import Flask,render_template,request,redirect
app = Flask(__name__)
@app.route('/Signup')
def siginup():
    return render_template("signup.html")

@app.route('/login')
def log1():
    return render_template("login.html")

def create_table():
    print("Opened database")
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute("drop table if exists users;")
    cur.execute('''CREATE TABLE users
         (
          name      TEXT    NOT NULL,
          email     TEXT     NOT NULL,
          username  TEXT     NOT NULL,
          password  TEXT     NOT NULL);''')
    print("A database table has been created now")

create_table()
def insertUser(name,email,username,password):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name,email,username,password) VALUES(?,?,?,?)", (name,email,username,password))
    conn.commit()

def retrieveUsers(username, password):
    conn = sql.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM users WHERE username=? AND password=?",(username, password))
    users = cur.fetchone()
    return users




@app.route('/Signup', methods=['POST'])
def home():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        username = request.form['username']
        password = request.form['password']
        insertUser(name,email,username,password)
        return redirect('/login')

@app.route('/login',methods=['POST'])
def log():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        account = retrieveUsers(username, password)
        if username in account:
            return redirect('/Signup')

if __name__ == '__main__':
    app.run(debug=True)
