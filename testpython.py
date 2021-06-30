#!/usr/bin/env python

from flask import Flask, render_template, request
from flask.helpers import total_seconds
import sqlite3
app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)

conn = None
cursor = None

@app.route('/')
def accueil():
    return render_template("home.html", message = "Connectez-vous")
@app.route('/', methods =['POST'])
def text_box():
    if request.method=="POST":
        mdp=request.form["mdp"]
        user_name=request.form["user_name"]
        connection = sqlite3.connect("base.db")
        conn = sqlite3.connect("base.db")
        cursor = conn.cursor()
        verisur=cursor.execute('SELECT * FROM base WHERE user_name =?',(user_name,))
        try:
            verif=cursor.fetchone()[0]
        except:
            total=0
        connection.close()
        if  verif==mdp:
            processed_text = text.upper()
            return render_template("bienvenue.html" , message = processed_text )
        else:
            processed_text = text.upper()
            return render_template("pasAcces.html", message = processed_text)
    else:
        print("hello")

@app.route('/new/', methods =['POST'])
def new_name():
    if request.method=="GET":
        nuser_name = request.form['nuser_name']
    if request.method=="POST":
        nmdp=request.form['nmdp']

if __name__ == "__main__":
    app.run(debug=True)

