from flask import (Flask, g, redirect, render_template, request)
from flask_cors import CORS
from actions.long_text import addLongTextToVectorDb
from actions.new_bot import addNewBot
from actions.response import getResponseFromAi
from dotenv import load_dotenv


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv()



@app.route("/")
def main():
    return render_template('long-text.html')

@app.route("/new/bot")
def new_bot():
    return render_template('new-bot.html')

@app.route("/api/long-text/add", methods=['POST'])
def api_long_text_add():
    text = request.form['text']
    id = request.form['id']
    addLongTextToVectorDb(text, id)
    return redirect('/')

@app.route("/api/response/get/<id>", methods=['GET'])
def api_response_get(id: str):
    question = request.args.get('question')
    return getResponseFromAi(question, id)

@app.route("/api/new/bot", methods=['POST'])
def api_new_bot():
    name = request.form['name']
    description = request.form['description']
    message = request.form['message']
    key = request.form['key']    
    return addNewBot(name, description, message, key)
    
