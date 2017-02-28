# coding=utf-8
from flask import Flask, g
from sqlite3 import IntegrityError
import sqlite3
import os

__author__ = 'Fredrik Håkansson (freha309)'

app = Flask(__name__)

DATABASE = path = os.path.dirname(os.path.abspath(__file__)) + '/database.db'
# DATABASE = 'C:\Users\Fredrik\Documents\git\lab2_tddd97\database.db'


# Initializes the database and are called at server startup
# Reads the queries stored in the 'database.schema' file
def init_database():
    with app.app_context():
        db = get_db()
        with app.open_resource('database.schema', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print "Database initialized"


# Returns the database object to execute queries
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g.database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Simplifies selecting data from Database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# Adds a user to the database
def add_user(email, password, firstname, familyname, gender, city, country):
    db = get_db()
    try:
        result = db.execute("INSERT INTO Users VALUES (?,?,?,?,?,?,?);", (email, password, firstname, familyname, gender, city, country))
        db.commit()
    except IntegrityError:
        return None

    return result


# Returns a sqlite3.Row with a user matching the email
# If no email is provided all users are returned
def find_user(email=None):
    if email is not None:
        result = query_db("SELECT * FROM Users WHERE email = ?",
                      (email,), one=True)
    else:
        result = query_db("SELECT * FROM Users")

    if result is None:
        return None
    else:
        return result


# Sets new password for the provided user
def update_password(email, password):
    db = get_db()
    result = db.execute("UPDATE Users SET password = ? WHERE email = ?", (password, email))
    db.commit()
    return result


# Fetches the user email corresponding to the provided token
def get_email_with_token(token):
    sql = "SELECT email FROM LoggedInUsers WHERE token=?"
    result = query_db(sql, (token,), one=True)
    return result


# Fetches user messages belonging to the provided email
def get_messages(email):
    result = query_db("SELECT id, author, message FROM Messages WHERE user=?", (email,))
    return result


# Adds a new message to a user (receiver)
def add_message(receiver, author, message):
    db = get_db()
    result = db.execute("INSERT INTO Messages (user, author, message) VALUES (?, ?, ?)", (receiver, author, message))
    db.commit()
    return result


# Adds token to database with corresponding user's email
def add_token(email, token):
    db = get_db()
    try:
        res = db.execute("INSERT INTO LoggedInUsers VALUES (?, ?);", (email, token))
        db.commit()
    except IntegrityError:
        res = db.execute("UPDATE LoggedInUsers SET token=? WHERE email=?", (token, email))
        db.commit()
    return res


# Removes token from database
def remove_token(token):
    db = get_db()
    res = db.execute("DELETE FROM LoggedInUsers WHERE token=?", (token,))
    db.commit()
    return res

