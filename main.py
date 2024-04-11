from flask import (Flask, g, redirect, render_template, request)
from flask_cors import CORS
from actions.long_text import addLongTextToVectorDb
from actions.response import getResponseFromAi
from dotenv import load_dotenv


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv()

@app.route("/")
def main():
    return render_template('long-text.html')

@app.route("/api/long-text/add", methods=['POST'])
def api_long_text_add():
    text = request.form['text']
    addLongTextToVectorDb(text)
    return redirect('/')

@app.route("/api/response/get/<text>", methods=['GET'])
def api_response_get(text: str):
    return getResponseFromAi(text)
    
