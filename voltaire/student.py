import functools

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from voltaire.db import get_db
from voltaire import languages

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
    return render_template("student/index.html", progress = progress, **languages[session["lang"]])

@bp.route("/settings", methods = ("GET", "POST"))
@student_login
def settings():
    dbLink = get_db().students.info

    if request.method == "POST":
        _grade = int(request.form["grade"])
        _class = request.form["class"]
        default_lang = request.form["lang"]

        dbLink.update_one({"_id": session["_id"]}, {"$set": {
            "grade": _grade,
            "class": _class,
            "lang": default_lang
        }})

        session["lang"] = default_lang
        #flash(f"It worked! {_grade} {_class} {default_lang}")

    return render_template("student/settings.html",**languages[session["lang"]])
