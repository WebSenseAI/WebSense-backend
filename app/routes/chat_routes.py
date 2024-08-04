
from flask import Blueprint, render_template, request, jsonify, redirect

from app.services.rag.chat import chat

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/bot/answer', methods=['GET'])
def get_response():
    data = request.args.to_dict()
    response = chat(data.get('id'), data.get('question'))
    return jsonify(response)