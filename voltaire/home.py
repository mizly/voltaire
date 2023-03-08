import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

#from werkzeug.security import check_password_hash, generatore_password_hash

#from flaskr.db import get_db

#__name__ passes name of this file, home.py
bp = Blueprint("home", __name__)

@bp.route("/")
def index():
    return render_template("home/index.html")