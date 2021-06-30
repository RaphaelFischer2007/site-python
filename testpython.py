#!/usr/bin/env python

from flask import Flask, render_template, request
from flask.helpers import total_seconds
import sqlite3
app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)
mdp=None
user_name=None
conn = None
cursor = None 
row=1

@app.route('/')
def accueil():
    return render_template("home.html", message = "Connexion")
@app.route('/', methods =['POST'])
def text_box():
    if request.method=="POST":
        user_name=request.form["user_name"]
        mdp=request.form["mdp"]
        print(user_name,mdp)
        connection = sqlite3.connect("base.db")
        conn = sqlite3.connect("base.db")
        cursor = conn.cursor()
        verif="SELECT mdp FROM base WHERE user_name =?"
        verif=cursor.execute (verif,([user_name]))
        verif=cursor.fetchone()
        connection.close()
        if verif != None:
            verif2="".join(verif)
            if  verif2==mdp:
                processed_text = user_name.upper()
                return render_template("bienvenue.html" , message = processed_text )
            else:
                processed_text = user_name.upper()
                return render_template("mauvaisMdp.html", message = processed_text)
        else:
                processed_text = user_name.upper()
                return render_template("mauvaisUser_name.html", message = processed_text)


@app.route('/new/', methods =['POST'])
def new_name():
    if request.method=="GET":
        nuser_name = request.form['nuser_name']
    if request.method=="POST":
        nmdp=request.form['nmdp']

if __name__ == "__main__":
    app.run(debug=True)

