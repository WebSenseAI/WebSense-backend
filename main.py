from flask import (Flask, g)
from database.connection import db, Vector
from database.functions import (getAllDbVectors)
from lang_chain.lang_chain import LangChainResponse
from os import path
from dotenv import load_dotenv
from chroma.chroma import get_all_db_vectors
app = Flask(__name__)

# Connect to the database
db.connect()
load_dotenv()



@app.route("/")
def main():
    return "<p>Hello, World!</p>"

@app.route("/chroma")
def chroma_api():  
    return get_all_db_vectors()   

@app.route("/api/<jsdata>")
def api_route(jsdata):
    db.create_tables([Vector])
    return LangChainResponse(jsdata)

@app.route("/api/db")
def api_route_all():
    return  getAllDbVectors("vector", db)