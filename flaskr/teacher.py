import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

#from werkzeug.security import check_password_hash, generatore_password_hash

#from flaskr.db import get_db

#__name__ passes name of this file, auth.py
bp = Blueprint("teacher", __name__, url_prefix = "/t")

@bp.route("/")
def index():
    return render_template("teacher/index.html")