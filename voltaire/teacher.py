import functools

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from voltaire import db

#from werkzeug.security import check_password_hash, generatore_password_hash

#__name__ passes name of this file, student.py
bp = Blueprint("teacher", __name__, url_prefix = "/t")

def teacher_login(function):
    def wrapper():
        if session.get("type") != "teacher":
            return abort(401)
        return function()
    
    # Rename the wrapper to work for multiple functions
    wrapper.__name__ = function.__name__
    return wrapper

@bp.route("/")
@teacher_login
def index():
    # Loads the student list into a dictionary
    dbLink = db.get_db().students.info
    studentList = [i for i in dbLink.find()]
    
    return render_template("teacher/index.html", students = studentList)

@bp.route("/settings/")
@teacher_login
def settings():
    return render_template("teacher/settings.html")

@bp.route("/view/")
@teacher_login
def view(_id):
    dbLink = db.get_db().students.info
    student = dbLink.find_one({"_id": _id})

    return render_template("teacher/view.html", student = student)