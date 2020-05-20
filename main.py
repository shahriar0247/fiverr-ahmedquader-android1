from flask import Flask, redirect, render_template, request, session, abort, send_from_directory, url_for
import webbrowser
import zipfile
import pymongo
import bcrypt
import datetime
import os
import sqlite3



app = Flask(__name__)

app.secret_key = os.urandom(12)

db = pymongo.MongoClient().xenusersdb
users = db.users




@app.route('/')
def home():
    if 'username' not in session:
        return render_template('login.html')
    else:
        return main()
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':

        login_user = users.find_one({'users': request.form['username']})
        
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
            
                return redirect(url_for('main'))
            return 'Invalid Password <a href="/login">Try again</a>'
        return 'User does not exists do you want to <a href="/register">Register</a>'

    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = users.find_one({'users':request.form['username']})
        if existing_user == None:
            if len(request.form['password']) < 63 and len(request.form['password']) > 7:
                hashedpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
           
                users.insert_one({'users':request.form['username'], 'password': hashedpass})
                return redirect(url_for('login'))
            return 'Please use a password more then 8 characters and less then 63 characters. <a href="/register">Try again.<a>'
        return 'User exists. <a href="/login">Login?<a>'

    elif request.method == 'GET':
        
        return render_template('register.html')

@app.route("/main", methods=["POST", "GET"])
def main():
    if request.method == "GET":
        return render_template("main.html")
    else:
        print(request.form["name"] + "asd")
        return render_template("main.html")

@app.route("/storeinfotodb", methods=["POST"])
def storeinfotodb():
    if request.method == "POST":
        conn = sqlite3.connect('database/allinfo.db')
        conn.execute("""CREATE TABLE IF NOT EXISTS requests (name text, description text)""")
        conn.execute("INSERT INTO requests VALUES ('"+request.form['name']+"', '"+request.form['description']+"','"+request.form['email']+"','"+request.form['number']+"'); ")
        conn.commit()
        conn.close()
        return redirect(url_for("main"))


@app.route("/showallinfo")
def showallinfo():
    conn = sqlite3.connect('database/allinfo.db')
    cursor = conn.execute("SELECT * FROM requests")
    all_req = cursor.fetchall()
    return render_template("showallinfo.html", all_req=all_req)

@app.route("/user")
def user():
    return render_template("user/main.html")

@app.route("/advertising")
def advertising():
    return render_template("user/advertising.html")
@app.route("/design")
def design():
    return render_template("user/design.html")


if __name__ == "__main__":
    app.run(host='3.1.5.104', port=4200, debug=True)
