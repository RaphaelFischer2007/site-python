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

@app.route('/connexion/', methods =['GET'])
def connexion():
    return render_template("connexion.html")

@app.route('/create/', methods =['GET'])
def create():
    return render_template("create.html")

@app.route('/')
def accueil():
    return render_template("home.html")

@app.route('/', methods =['POST'])
def text_box():
    if request.method=="POST":
        text_box.user_name=request.form["user_name"]
        mdp=request.form["mdp"]
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
    if exist == None and exist != "base" and exist != "sqlite_sequence":
        if nuser_name !="":
            if nmdp != "":
                connection = sqlite3.connect("base.db")
                cursor = connection.cursor()
                new_user=(nuser_name,nmdp,cursor.lastrowid)
                cursor.execute('INSERT INTO base VALUES (?,?,?)', new_user)
                conn = sqlite3.connect("base.db")
                cursor.execute('''CREATE TABLE IF NOT EXISTS {} (
                friend TEXT,
                "id" INTEGER,PRIMARY KEY("id" AUTOINCREMENT)
                )'''.format(nuser_name))
                friend_request=nuser_name+"_request"
                cursor.execute('''CREATE TABLE IF NOT EXISTS {} (
                friend_request TEXT,
                "id" INTEGER,PRIMARY KEY("id" AUTOINCREMENT)
                )'''.format(friend_request))
                your_request="your_"+friend_request
                cursor.execute('''CREATE TABLE IF NOT EXISTS {} (
                your_request TEXT,
                "id" INTEGER,PRIMARY KEY("id" AUTOINCREMENT)
                )'''.format(your_request))
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

@app.route('/backb/', methods =['GET'])
def backb():
    return render_template("bienvenue.html")

@app.route('/backc/', methods =['GET'])
def backc():
    return render_template("connexion.html")

@app.route('/backf/', methods =['GET'])
def backf():
    return render_template("friends.html")

@app.route('/delete/', methods =['GET'])
def delete():
    connection = sqlite3.connect("base.db")
    cursor = connection.cursor()
    
    user_name="".join(text_box.user_name)
    id=cursor.execute('SELECT id FROM base WHERE user_name =?', (user_name,))
    id=cursor.fetchone()
    cursor.execute('DELETE FROM base WHERE id=?',id)
    cursor.execute('''DROP TABLE {}'''.format(user_name))
    friend_request=user_name+"_request"
    cursor.execute('''DROP TABLE {}'''.format(friend_request))
    connection.commit()
    connection.close()
    return render_template("home.html")

@app.route('/friend_request/',methods=['GET'])
def friend_requets():
    connection = sqlite3.connect("base.db")
    cursor = connection.cursor()
    user_name = text_box.user_name
    user_request = user_name+"_request"
    your_request="your_"+user_request
    request_or_not=cursor.execute('SELECT * FROM {} '.format(your_request))
    request_or_not=cursor.fetchone()
    if request_or_not != None:
        request_or_not=cursor.execute('SELECT * FROM {}'.format(user_request))
        request_or_not=cursor.fetchone()
        if request_or_not != None:
            text_box.maybe_friend=cursor.execute('SELECT friend_request FROM {} ORDER BY RANDOM() LIMIT 1'.format(user_request))
            text_box.maybe_friend=cursor.fetchone()
            maybe_friend="".join(text_box.maybe_friend)
            connection.close()
            return render_template("friend_request.html", message=maybe_friend)
        else:
            text_box.maybe_friend=cursor.execute('SELECT id FROM {} ORDER BY RANDOM() LIMIT 1'.format(your_request))
            text_box.maybe_friend=cursor.fetchone()
            his_request=text_box.maybe_friend+"_request"
            accepted_or_not=cursor.execute('SELECT id FROM {} WHERE friend_request =?'.format(his_request),text_box.user_name)
            accepted_or_not=cursor.fetchone()
            if accepted_or_not != None:
                connection.close()
                return render_template("dont-know.html", message=text_box.maybe_friend)
            else:
                accepted_or_not=cursor.execute('SELECT id FROM {} WHERE friend =?'.format(text_box.maybe_friend),)
                if accepted_or_not != None:
                    connection.close()
                    return render_template("refused.html", message=text_box.maybe_friend)
                else:
                    connection.close()
                    return render_template("accepted.html", message=text_box.maybe_friend)
    else:
        request_or_not=cursor.execute('SELECT * FROM {}'.format(user_request))
        request_or_not=cursor.fetchone()
        if request_or_not != None:
            text_box.maybe_friend=cursor.execute('SELECT friend_request FROM {} ORDER BY RANDOM() LIMIT 1'.format(user_request))
            text_box.maybe_friend=cursor.fetchone()
            maybe_friend="".join(text_box.maybe_friend)
            connection.close()
            return render_template("friend_request.html", message=maybe_friend)
        else:
            return render_template("no_request.html")


@app.route('/accept/', methods=['GET'])
def accept():
    connection=sqlite3.connect("base.db")
    cursor=connection.cursor()
    user_request=text_box.user_name+"_request"
    maybe_friend="".join(text_box.maybe_friend)
    query = 'DELETE FROM '+user_request+' WHERE friend_request=\"'+maybe_friend+"\""
    connection.execute(query)
    user_name="".join(text_box.user_name)
    cursor.execute('INSERT INTO '+user_name+'(friend,id) VALUES ("'+maybe_friend+'","'+cursor.lastrowid+'")')
    connection.commit()
    connection.close()
    return render_template("friend_request.html")

@app.route('/refuse/', methods=['GET'])
def refuse():
    connection=sqlite3.connect("base.db")
    cursor=connection.cursor()
    user_request=text_box.user_name+"_request"
    maybe_friend="".join(text_box.maybe_friend)
    query = 'DELETE FROM '+user_request+' WHERE friend_request=\"'+maybe_friend+"\""
    connection.execute(query)
    connection.commit()
    connection.close()
    return render_template("friend_request.html")

@app.route('/new_friend/',methods=['GET'])
def new_friends():
    return render_template("new_friend.html")

@app.route('/friends/',methods=['GET'])
def friends():
    return render_template("friends.html")

@app.route('/new_friend/',methods=['GET'])
def new_friend():
    return render_template("new_friend.html")

@app.route('/add_friend/', methods=['POST'])
def add_friend():
    friend_name=request.form["friend_name"]
    connection = sqlite3.connect("base.db")
    if friend_name != text_box.user_name:
        cursor = connection.cursor()
        id=cursor.execute('SELECT id FROM base WHERE user_name =?', (friend_name,))
        id=cursor.fetchone()
        if id != None :
            friend_request=friend_name+"_request"
            id=cursor.execute('SELECT MAX(id) FROM {}'.format(friend_request))
            id=cursor.fetchone()
            id=cursor.fetchone()
            cursor.execute('INSERT INTO {} VALUES (?,?)'.format(friend_request), (text_box.user_name,id))
            user_request=text_box.user_name+"_request"
            your_request="your_"+user_request
            cursor.execute('INSERT INTO {} VALUES (?,?)'.format(your_request), (friend_name,cursor.lastrowid))
            connection.commit()
            connection.close()
            return render_template("friendship_created.html", message=friend_name)
        else :
            connection.close()
            return render_template("cant_add.html", message=friend_name)
    else :
        connection.close()
        return render_template("add_yourself.html", message=friend_name)

if __name__ == "__main__":
    app.run(debug=True)
