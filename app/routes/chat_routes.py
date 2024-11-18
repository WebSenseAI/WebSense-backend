from flask import Blueprint, render_template, request, jsonify, redirect

from concurrent.futures import ThreadPoolExecutor
from app.services.rag.chat import chat
from app.services.database.chat_db import insert_new_question
from app.services.database.geocountry_localdb import get_requester_country

chat_bp = Blueprint('chat_bp', __name__)

executor = ThreadPoolExecutor()

@chat_bp.route('/bot/answer', methods=['GET'])
def get_response():
    data = request.args.to_dict()
    botid = data.get('id')
    question = data.get('question')
    response = chat(botid, question)

    ip_address = request.access_route[0]
    metadata = {
        'ip_address' : ip_address,
        'method': request.method,
        'url': request.url,
        'path': request.path,
        'host': request.host,
        'user_agent': request.headers.get('User-Agent'),
        'accept_language': request.headers.get('Accept-Language'),
        'accept_encoding': request.headers.get('Accept-Encoding'),
        'referer': request.headers.get('Referer'),
        'content_type': request.headers.get('Content-Type'),
        'country' : get_requester_country(ip_address)
    }


    executor.submit(insert_new_question, botid, question, response, metadata)
    # insert_new_question(bot_id=botid, question=question, response=response)
    return jsonify(response)