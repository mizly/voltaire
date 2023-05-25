import functools

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from voltaire import db

#from werkzeug.security import check_password_hash, generatore_password_hash

#__name__ passes name of this file, student.py
bp = Blueprint("student", __name__, url_prefix = "/s")

def student_login(function):
    def wrapper():
        if session.get("type") != "student":
            return abort(401)
        return function()
    
    # Rename the wrapper to work for multiple functions
    wrapper.__name__ = function.__name__
    return wrapper

@bp.route("/")
@student_login
def index():
    dbLink = db.get_db().students.progress
    progress = dbLink.find_one({"_id": session["_id"]})
    return render_template("student/index.html", progress = progress)

@bp.route("/welcome/")
@student_login
def welcome():
    return render_template("student/welcome.html")

@bp.route("/settings/")
@student_login
def settings():
    return render_template("student/settings.html")