import os
from flask import (Flask, g, jsonify, redirect, render_template, request, session)
from flask_cors import CORS
from actions.bot_info import getBotById, getUserIdBot
from actions.long_text import addLongTextToVectorDb
from actions.new_bot import addNewBot
from actions.response import getResponseFromAi
from dotenv import load_dotenv
from auth.auth import login, authorize
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS
from swagger_ui import api_doc
import os

app = Flask(__name__)
if os.environ.get('FLASK_ENV') == 'development':
    print("DEVELOPMENT SERVER")
    CORS(app,
         resources={r"/*": {"origins": "http://localhost:5173"}},
         supports_credentials=True)
else:
    CORS(app,
         resources={r"/*": {"origins": "https://websenseai.netlify.app"}},
         supports_credentials=True)



api_doc(app, config_path='./swagger.yaml', url_prefix='/api/doc', title='API doc')

app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = '123456789'
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
)

oauth = OAuth(app)

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

@app.route("/api/response/get/<id>", methods=['POST'])
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
    user_id = request.json['user_id']
    return addNewBot(name, website, description, message, key, user_id)

@app.route("/api/info/bot/<id>", methods=['GET'])
def api_get_bot(id: str): 
    return getBotById(id)
    
    
# OAuth routes
@app.route("/login")
def login_oauth():
    return login(oauth)

@app.route("/authorize")
def login_authorize():
    return authorize(oauth)

@app.route("/userinfo")
def get_user_info():
    if 'user_info' in session:
        return jsonify(dict(session['user_info']))
    else:
        return "No user info in session", 400
    
@app.route("/api/user/bot/<id>", methods=['GET']) # TODO: check if this is the correct route similar to /api/info/bot/<id>
def get_user_bot(id: str):
    bot_id = getUserIdBot(id)
    if bot_id['bot_id'] == None:
        return {
            'bot_id': None
        }
    return getBotById(bot_id['bot_id'])
