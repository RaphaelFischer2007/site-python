#!/usr/bin/env python

from flask import Flask, render_template, request, session
from flask.helpers import total_seconds
import sqlite3
app = Flask(__name__)

app.config.update()
TESTING=True,
SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'

cursor = None 
row=1

@app.route('/')
def accueil():
    return render_template("home.html")

@app.route('/', methods =['POST'])
def text_box():
    if request.method=="POST":
        text_box.user_name=request.form["user_name"]
        mdp=request.form["mdp"]
        print (text_box.user_name,mdp)
        connection = sqlite3.connect("base.db")
        conn = sqlite3.connect("base.db")
        cursor = conn.cursor()
        verif="SELECT mdp FROM base WHERE user_name =?"
        verif=cursor.execute (verif,([text_box.user_name]))
        verif=cursor.fetchone()
        connection.close()
        if verif != None:
            verif2="".join(verif)
            if  verif2==mdp:
                processed_text = text_box.user_name.upper()
                return render_template("bienvenue.html", user_name = text_box.user_name)
            else:
                return render_template("mauvaisMdp.html")
        else:
                return render_template("mauvaisUser_name.html")

@app.route('/new/', methods =['POST'])
def new_name():
    nuser_name = request.form['nuser_name']
    nmdp=request.form['nmdp']
    connection = sqlite3.connect("base.db")
    conn = sqlite3.connect("base.db")
    cursor = conn.cursor()
    exist="SELECT mdp FROM base WHERE user_name =?"
    exist=cursor.execute (exist,([nuser_name]))
    exist=cursor.fetchone()
    connection.close()
    if exist == None:
        if nuser_name !="":
            if nmdp != "":
                connection = sqlite3.connect("base.db")
                cursor = connection.cursor()
                new_user=(nuser_name,nmdp,cursor.lastrowid)
                cursor.execute('INSERT INTO base VALUES (?,?,?)', new_user)
                connection.commit()
                connection.close()
                return render_template("account_created.html")
            else:
                return render_template("use_a_password.html")
        else:
            return render_template("use_a_user_name.html")
    else:
        return render_template("account_already_exist.html")

@app.route('/return/', methods =['GET'])
def gohome():
    return render_template("home.html")

@app.route('/delete/', methods =['GET'])
def delete():
    connection = sqlite3.connect("base.db")
    cursor = connection.cursor()
    user_name="".join(text_box.user_name)
    print(user_name)
    id=cursor.execute('SELECT id FROM base WHERE user_name =?', (user_name,))
    id=cursor.fetchone()
    print(id)
    cursor.execute('DELETE FROM base WHERE id=?',id)
    connection.commit()
    connection.close()
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)

