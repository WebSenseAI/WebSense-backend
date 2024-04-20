from flask import (Flask, g, redirect, render_template, request)
from flask_cors import CORS
from actions.bot_info import getBotById
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
    name = request.json['name']
    website = request.json['website']
    description = request.json['description']
    message = request.json['message']
    key = request.json['key']    
    return addNewBot(name, website, description, message, key)

@app.route("/api/info/bot/<id>", methods=['GET'])
def api_get_bot(id: str): 
    return getBotById(id)
    
    
""" 1d4c9e61-ab90-4d15-afe5-0d56e786be74 """