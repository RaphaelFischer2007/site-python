#!/usr/bin/env python

from flask import Flask, render_template, request
from flask.helpers import total_seconds



app = Flask(__name__)

admis = ['Raphael','raphael']

@app.route('/')
def hello():
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
            return render_template("pasAcces.html")

if __name__ == "__main__":
    app.run(debug=True)