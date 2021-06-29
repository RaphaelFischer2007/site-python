#!/usr/bin/env python

from flask import Flask, render_template, request
from flask.helpers import total_seconds

app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)

admis = ['Raphael','raphael']

@app.route('/')
def accueil():
    return render_template("home.html", message = "Indiquez votre prénom")

@app.route('/', methods =['POST'])
def text_box():
    if request.method=="POST":
        text = request.form['text']
        if text in admis:
            processed_text = text.upper()
            return render_template("bienvenue.html" , message = processed_text )
        else:
            processed_text = text.upper()
            return render_template("pasAcces.html", message = processed_text)

@app.route('/new/', methods =['POST'])
def new_name():
    if request.form['nouveau'] in admis :
        admis.remove(request.form['nouveau'])
        return render_template("home.html", message = "Indiquez votre prénom" )
    else:
        admis.append(request.form['nouveau'])
        return render_template("home.html", message = "Indiquez votre prénom" )


if __name__ == "__main__":
    app.run(debug=True)