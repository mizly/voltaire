import functools

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from voltaire.db import get_db

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
    dbLink = get_db().students.progress
    progress = dbLink.find_one({"_id": session["_id"]})
    return render_template("student/index.html", progress = progress)

@bp.route("/welcome/", methods = ("GET", "POST"))
@student_login
def welcome():

    dbLink = get_db().students.info

    if request.method == "POST":
        print("u")
        _grade = request.form["grade"]
        _class = request.form["class"]

        dbLink.update_one({"_id": session["_id"]}, {"$set": {"grade": _grade, "class": _class}})
        
        return redirect(url_for("student.index"))

    _id = dbLink.find_one({"_id": session["_id"]})
    return render_template("student/welcome.html", profile = _id)

@bp.route("/settings/", methods = ("GET", "POST"))
@student_login
def settings():
    return render_template("student/settings.html")