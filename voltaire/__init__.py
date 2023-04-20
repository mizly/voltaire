#Least scuffed import
import json
import os
import pathlib

import requests
from flask import Flask, abort, g, session, redirect, request
from pymongo import MongoClient
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

#to allow http traffic for local dev
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

with open("voltaire\database.json","r") as f:
    #instantiates reference to mongdb server (the server contains the databases)
    j = json.load(f)
    client = MongoClient(j["connection"])

sdb = client.students
sidb = sdb.info
spdb = sdb.progress

tdb = client.teachers
tidb = tdb.info

cdb = client.classes

GOOGLE_CLIENT_ID = "158531260771-q7vopkn3fu0l3gk6ar5s6vn9mr4s3aa1.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback"
)

def create_app(test_config = None):
    """
    Application factory that can be instantiated multiple times simultaneously, generally for testing.

    Parameters:
        None

    Returns:
        app: the flask app to instantiate
    """
    app = Flask(__name__, instance_relative_config = True)

    #secrets!
    with open("voltaire\client_secret.json","r") as f:
        j = json.load(f)["web"]
        GOOGLE_CLIENT_ID = j["client_id"]
        app.config.from_mapping(
            SECRET_KEY = j["client_secret"],
            #DATABASE = os.path.join(app.instance_path, 'voltaire.sqlite'),
        )
    
    print(GOOGLE_CLIENT_ID,app.secret_key) #HEYYY DON'T FORGET ABOUT THIS! -------------------------------------------------------------------
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def login_is_required(function):
        def wrapper():
            if "_id" not in session:
                return abort(401)  # Authorization required
            else:
                return function(g.type)
        return wrapper
    
    @app.before_request
    def load_user():
        #Primarily used for loading a page with specific characteristics
        g.lang = session.get("lang") #temporarily unchangeable during development
        g.user = session.get("name")
        g.type = session.get("type")

    @app.route("/login")
    def login():
        print("login")
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)
    
    @app.route("/callback")
    def callback():
        print("callback")
        flow.fetch_token(authorization_response = request.url)
        #if not session["state"] == request.args["state"]: #the problem is that session is not being saved globally
        #    abort(500)  # State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=2
        )

        print("if")
        #Checks if the login is a new user
        if sidb.find_one({"_id": id_info.get("sub")}) is None and tidb.find_one({"_id": id_info.get("sub")}) is None:
            new_user = {
                "_id": id_info.get("sub"),
                "give_name": id_info.get("given_name"),
                "family_name": id_info.get("family_name"),
                "grade": None,
                "class": ""
            }

            #New teachers are added elsewhere
            sidb.insert_one(new_user)

        print("pas if")
        #Fetches the
        if (entry := sidb.find_one({"_id": id_info.get("sub")})) is not None:
            print(entry)
            session["type"] = "student"
            for key in entry:
                session[key] = entry[key]
        elif (entry := tidb.find_one({"_id": id_info.get("sub")})) is not None:
            session["type"] = "teacher"
            for key in entry:
                session[key] = entry[key]

        print(session)

        return redirect("/account")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")
    
    @app.route("/account")
    @login_is_required
    def account(user_type):
        if user_type == "teacher":
            return redirect("/t/")
        elif user_type == "student":
            return redirect("/s/")

    from voltaire import home, student, teacher

    app.register_blueprint(student.bp)
    app.register_blueprint(teacher.bp)
    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint = "index")
    
    return app