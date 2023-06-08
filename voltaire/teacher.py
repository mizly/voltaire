import functools

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from voltaire import db
from voltaire import languages

#__name__ passes name of this file, student.py
bp = Blueprint("teacher", __name__, url_prefix = "/t")

def teacher_login(function):
    def wrapper(**kwargs):
        if session.get("type") != "teacher":
            return abort(401)

        # Check if arguments should be passed to the view function
        if kwargs != {}:
            return function(**kwargs)

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

    return render_template("teacher/index.html", students = studentList, **languages[session["lang"]])

@bp.route("/settings/")
@teacher_login
def settings():
    return render_template("teacher/settings.html", **languages[session["lang"]])

@bp.route("/view/<_id>", methods = ("GET", "POST"))
@teacher_login
def view(_id):
    dbLink = db.get_db().students
    student_info = dbLink.info
    student_progress = dbLink.progress


    if request.method == "POST":
        print("among us", request.form)
        for i in request.form:
            student_progress.update_one({"_id": _id}, {"$set": {i: int(request.form[i])}})

    # Retrieve the data after any potential updates to it
    student = student_info.find_one({"_id": _id})
    print(student)
    progress = student_progress.find_one({"_id": _id})
    return render_template("teacher/view.html", student_name = student["given_name"], progress = progress, **languages[session["lang"]])
