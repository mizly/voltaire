import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from voltaire import languages

#__name__ passes name of this file, home.py
bp = Blueprint("home", __name__)

@bp.route("/")
def index():
    return render_template("home/index.html", **languages[session["lang"]])
