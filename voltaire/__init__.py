# Generic libraries
import json
import os
import pathlib
import locale
from glob import glob

# Flask library
from flask import Flask, abort, g, session, redirect, request

# Google API libraries
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from pip._vendor import cachecontrol
import requests

# Allow http traffic for local dev
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "158531260771-q7vopkn3fu0l3gk6ar5s6vn9mr4s3aa1.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

languages = {}
language_list = glob("voltaire/lang/*.json")
for lang in language_list:
    filename = lang.split('\\')
    lang_code = filename[1].split('.')[0]

    with open(lang, 'r', encoding='utf8') as file:
      languages[lang_code] = json.loads(file.read())

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback"
)

def create_app(test_config = None):
    """
    Application factory containing the Flask app. Can be instantiated multiple times simultaneously, generally for testing.

    Parameters:
        None

    Returns:
        app: the flask app to instantiate
    """
    app = Flask(__name__, instance_relative_config = True)

    # Configuring secret variables
    with open("voltaire\client_secret.json","r") as f:
        j = json.load(f)["web"]
        GOOGLE_CLIENT_ID = j["client_id"]
        app.config.from_mapping(
            SECRET_KEY = j["client_secret"],
        )

    # Check if a testing configuration is passed, and load it if so
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
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

    @app.before_first_request
    def preset():
        session["lang"] = "en_CA"
        session["type"] = "home"

    @app.before_request
    def load_user():
        # Primarily used for loading a page with specific characteristics
        if session.get("lang") is None:
            session["lang"] = "en_CA"
        g.lang = session.get("lang") # temporarily unchangeable during development
        g.user = session.get("_id")
        g.type = session.get("type")

    @app.route("/en")
    def en():
        session["lang"] = "en_CA"
        return redirect(request.referrer)

    @app.route("/fr")
    def fr():
        session["lang"] = "fr_CA"
        return redirect(request.referrer)

    @app.route("/login")
    def login():
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)

    @app.route("/callback")
    def callback():
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

        # Load the databse connection
        dbLink = db.get_db()
        sdb = dbLink.students
        sidb = sdb.info
        spdb = sdb.progress

        tdb = dbLink.teachers
        tidb = tdb.info

        #cdb = dbLink.classes

        # Checks if the login is a new user, and creates a new profile if so
        if sidb.find_one({"_id": id_info.get("sub")}) is None and tidb.find_one({"_id": id_info.get("sub")}) is None:
            isTeacher = False
            with open("voltaire\database.json","r") as f:
                j = json.load(f)
                if id_info.get("email") in j["teachers"]:
                    isTeacher = True

            if isTeacher:
                tidb.insert_one(account.new_teacher(id_info))

            else:
                sidb.insert_one(account.new_student(id_info))
                spdb.insert_one(account.new_progress(id_info))

        # Fetches the user's information and stores it in the session
        if (entry := sidb.find_one({"_id": id_info.get("sub")})) is not None:
            session["type"] = "student"
        elif (entry := tidb.find_one({"_id": id_info.get("sub")})) is not None:
            session["type"] = "teacher"

        for key in entry:
            session[key] = entry[key]

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

    from voltaire import account, db, home, student, teacher

    db.init_app(app)
    app.register_blueprint(student.bp)
    app.register_blueprint(teacher.bp)
    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint = "index")

    return app
