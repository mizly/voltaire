import functools

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for

#from werkzeug.security import check_password_hash, generatore_password_hash

#from flaskr.db import get_db

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
    return render_template("teacher/index.html")