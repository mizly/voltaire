#Least scuffed import
import json
import os
import pathlib

#Clean this up at some point
import requests
from flask import Flask, abort, g, session, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from voltaire.db import get_db

#to allow http traffic for local dev
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

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
        g.user = session.get("_id")
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

        db = get_db()
        print(db)
        sdb = db.students
        sidb = sdb.info
        spdb = sdb.progress

        tdb = db.teachers
        tidb = tdb.info

        cdb = db.classes

        #Checks if the login is a new user
        if sidb.find_one({"_id": id_info.get("sub")}) is None and tidb.find_one({"_id": id_info.get("sub")}) is None:
            new_user = {
                "_id": id_info.get("sub"),
                "given_name": id_info.get("given_name"),
                "family_name": id_info.get("family_name"),
                "grade": None,
                "class": ""
            }

            progress = {
                "_id": id_info.get("sub"),
                "1a": {
                    "avoir/etre/il y a": 0,
                    "les articles": 0,
                    "pronoms sujets": 0,
                    "les mots interrogatifs": 0
                },
                "1b": {
                    "present regulier": 0,
                    "la negation": 0,
                    "adjectif regulier + emploi": 0,
                    "les prepositions 1": 0,
                    "les mots liens 1": 0
                },
                "2a": {
                    "present": 0,
                    "futur proche": 0,
                    "les adverbes": 0,
                    "interrogation inverse": 0
                },
                "2b": {
                    "adjectifs possessifs et demonstratifs": 0,
                    "verbes pronominaux": 0,
                    "adjectifs": 0,
                    "les prepositions 2": 0,
                    "imperatif": 0
                },
                "3a": {
                    "comparatif et superlatif": 0,
                    "adjectifs irreguliers": 0,
                    "adverbes": 0,
                    "jouer a, de + fare de": 0
                },
                "3b": {
                    "les mots lien 2": 0,
                    "complements d'object direct": 0,
                    "passe compose reguliers": 0,
                    "futur simple": 0
                },
                "4a": {
                    "present oir": 0,
                    "imperatif employe avec cod": 0,
                    "present avec changement orthographique": 0,
                    "la negation du passse compose": 0,
                },
                "4b": {
                    "les participes passes irreguliers + pronominaux + negation": 0,
                    "imparfait + engation": 0,
                    "completions d'object indirect": 0,
                    "conditionnel present": 0
                },
                "5a": {
                    "concordance des temps 1": 0,
                    "imperatif employe avec coi": 0,
                    "phrases de conditions 1": 0,
                    "y et en": 0
                },
                "5b": {
                    "verbes avec prepositions": 0,
                    "passe compose avec cod + accord": 0,
                    "subjonctif 1": 0
                },
                "6a": {
                    "pronoms possessifs et relatifs": 0,
                    "les mots liens 3": 0,
                    "participe passe employe comme adjectif": 0,
                    "subjonctif 2": 0
                },
                "6b": {
                    "participe present": 0,
                    "plus-que-parfait": 0,
                    "futur anterieur": 0,
                    "conditionnel passe": 0,
                    "subjonctif 3": 0
                },
                "7a": {
                    "pronoms relatifs composes": 0,
                    "concordance des temps 2": 0,
                    "subjonctif 4": 0
                },
                "7b": {
                    "subjonctif 5": 0,
                    "phrases de condition 2": 0
                },
                "8a": {
                    "pronoms demonstratifs": 0,
                    "passe simple - emploi": 0,
                    "subjonctif 6": 0
                },
                "8b": {
                    "gerondif et adjectif verbal": 0,
                    "concordance des modes": 0
                },
                "9a": {
                    "gerondif et adjectif verbal - participe present": 0,
                    "passe simple - emploi dans un texte": 0,
                    "subjonctif passe 1": 0
                },
                "9b": {
                    "la voix passive": 0,
                    "subjonctif passe 2": 0
                }
            }

            #New teachers are added elsewhere
            sidb.insert_one(new_user)
            spdb.insert_one(progress)

        #Fetches the user's information and stores it in the session
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

    from voltaire import db, home, student, teacher

    db.init_app(app)

    app.register_blueprint(student.bp)
    app.register_blueprint(teacher.bp)
    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint = "index")
    
    return app