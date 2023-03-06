#Least scuffed import
import os
import pathlib
import json

import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

GOOGLE_CLIENT_ID = "158531260771-q7vopkn3fu0l3gk6ar5s6vn9mr4s3aa1.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback"
)

"""
Application factory that can be instantiated multiple times simultaneously, generally for testing.

Parameters:
    None

Returns:
    app: the flask app to instantiate
"""
def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)

    #secrets!
    with open("voltaire\client_secret.json","r") as f:
        g = json.load(f)["web"]
        GOOGLE_CLIENT_ID = g["client_id"]
        app.config.from_mapping(
            SECRET_KEY=g["client_secret"],
            #DATABASE=os.path.join(app.instance_path, 'voltaire.sqlite'),
        )

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
        def wrapper(*args, **kwargs):
            if "google_id" not in session:
                return abort(401)  # Authorization required
            else:
                return function()
        return wrapper

    @app.route("/")
    def index():
        return "This is the home page <a href='/login'><button>Login</button></a>"

    @app.route("/login")
    def login():
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)
    
    @app.route("/callback")
    def callback():
        flow.fetch_token(authorization_response=request.url)
        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        domain = (id_info.get("email"))
        print(session,domain)
        if "@ocdsb.ca" in domain:
            print("User is part of ocdsb.")
        return redirect("/account")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")
    
    @app.route("/account")
    @login_is_required
    def account():
        return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"

    from voltaire import home, student, teacher

    app.register_blueprint(student.bp)
    app.register_blueprint(teacher.bp)
    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint = "index")
    
    return app
