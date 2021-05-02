import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/Signup')
def siginup():
    return render_template("signup.html")

@app.route('/login')
def log1():
    return render_template("login.html")

def create_table():
    print("Opened database")
    conn = sqlite.connect('database.db')
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
    conn = sqlite.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name,email,username,password) VALUES(?,?,?,?)", (name,email,username,password))
    conn.commit()

def retrieveUsers(username, password):
    conn = sqlite.connect('database.db')
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
            return redirect('/predict')

@app.route('/predict')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    if (prediction[0]==1):
        output = 'Yes'
    else:
        output = 'No'
    return render_template('index.html', prediction_text='Will you repay the loan: {}'.format(output))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
 