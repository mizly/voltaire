import functools

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from voltaire import db
#from werkzeug.security import check_password_hash, generatore_password_hash

#__name__ passes name of this file, auth.py
bp = Blueprint("student", __name__, url_prefix = "/s")

def student_login(function):
    def wrapper():
        if session["type"] != "student":
            return abort(401)
        return function()
    return wrapper

@bp.route("/")
@student_login
def index():
    return render_template("student/index.html")