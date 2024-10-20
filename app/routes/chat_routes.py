from flask import Blueprint, render_template, request, jsonify, redirect

from concurrent.futures import ThreadPoolExecutor
from app.services.rag.chat import chat
from app.services.database.chat_db import insert_new_question

chat_bp = Blueprint('chat_bp', __name__)

executor = ThreadPoolExecutor()

@chat_bp.route('/bot/answer', methods=['GET'])
def get_response():
    data = request.args.to_dict()
    botid = data.get('id')
    question = data.get('question')
    response = chat(botid, question)

    executor.submit(insert_new_question, botid, question, response)
    # insert_new_question(bot_id=botid, question=question, response=response)
    return jsonify(response)