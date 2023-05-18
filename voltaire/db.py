import json
from pymongo import MongoClient
from flask import current_app, g
#You learn something new about imports every day

def get_db():
    if "db" not in g:
        with open("voltaire\database.json","r") as f:
            #instantiates reference to mongdb server (the server contains the databases)
            j = json.load(f)
            #g.db = MongoClient(j["connection"])
            g.db = MongoClient()
        
        return g.db

def close_db(e = None):
    #Create identifier to see if db was an entry that was popped
    #Second arg None tells program to not return error
    db = g.pop("db", None)
    print("db", db)
    #Close the actual connection if the corresponding g entry was closed
    if db is not None:
        db.close()

def init_db():
    #Just open the db. nothing else
    db = get_db()

def init_app(app):
    #The factory calls this function before starting the app
    #app.teardown_appcontext sets the function to call after each application context as close_db()
    app.teardown_appcontext(close_db)