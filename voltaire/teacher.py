import functools

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from voltaire import db

#from werkzeug.security import check_password_hash, generatore_password_hash

#__name__ passes name of this file, auth.py
bp = Blueprint("teacher", __name__, url_prefix = "/t")

def teacher_login(function):
    def wrapper():
        if session["type"] != "teacher":
            return abort(401)
        return function()
    return wrapper

@bp.route("/")
@teacher_login
def index():
    # Loads the student list into a dictionary
    dbLink = db.get_db().students.info
    studentList = [i for i in dbLink.find()]
    
    return render_template("teacher/index.html", students = studentList)