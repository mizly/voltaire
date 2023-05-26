import json
from pymongo import MongoClient
from flask import g

def get_db():
    """
    Creates a connection to the MongoDB database.

    Parameters:
        None

    Returns:
        None
    """
    if "db" not in g:
        with open("voltaire\database.json","r") as f:
            # Instantiates reference to mongdb server (the server contains the databases)
            #j = json.load(f)
            #g.db = MongoClient(j["connection"])
            g.db = MongoClient()

        return g.db

def close_db(e = None):
    """
    Closes the connection to the MongoDB database.

    Parameters:
        e (default None): the error to handle, if applicable

    Returns:
        None
    """
    # Creates identifier to see if db was an entry that was popped
    # None is what the program returns if not
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_app(app):
    """
    Creates a connection to the MongoDB database. Called during app initialization.

    Parameters:
        app: the app being passed

    Returns:
        None
    """
    # Tells Flask to call close_db() after each application context
    app.teardown_appcontext(close_db)
