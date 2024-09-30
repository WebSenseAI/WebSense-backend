from flask import Blueprint, request, jsonify
from app.constants.http_status_codes import SUCCESS_CODE
from app.services.supabase_client_utils import get_user_info
from app.services.database.bots_db import create_new_bot, get_user_bot, get_bot_by_id, remove_user_bot
from app.errors.http_error_templates import create_returnable_internal_error_template
from app.constants.internal_errors import InternalErrorCode
from app.services.ai_tools.vectors import add_text_to_vector_db
from app.services.ai_tools.openai_utils import get_embedding
from app.services.ai_tools.text import split_multiple_texts
from app.services.webscraping.scrapWrapper import trainNewBot
from app.extensions import supabase
from app.models.vector_model import VectorModel
from app.security import authorization_required

# Blueprint for user routes

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/userinfo')
@authorization_required
def userinfo():
    userinfo = get_user_info(request.authorization.token)
    return jsonify(userinfo.model_dump()), SUCCESS_CODE
    
    
@users_bp.route('/bot/new', methods=['POST'])
@authorization_required
def create_bot():
    data = request.json
    access_token = request.authorization.token
    response = create_new_bot(
        access_token=access_token,
        name = data['name'],
        website_url=data['website'],
        description=data['description'],
        first_message=data['message'],
        openai_key=data['key']
    )
    botid = response[0]["id"]

    pages = trainNewBot(data['website'], False)
    
    splitted_text = split_multiple_texts(pages)

    embeddings = get_embedding(splitted_text)
    
    vector_model = VectorModel(splitted_text,embeddings)
    
    add_text_to_vector_db(vector_model, botid)
    print('FINITO')
    return {}, SUCCESS_CODE


@users_bp.route('/bot/info', methods=['GET'])
@authorization_required
def get_bot_info_by_user():
    user = get_user_info(request.authorization.token)
    userid = user.id
    bot_info = get_user_bot(userid)
    if not bot_info:
        return create_returnable_internal_error_template(InternalErrorCode.BotNotExist)
    
    return jsonify(bot_info[0]), SUCCESS_CODE


@users_bp.route('/bot/info/<botid>', methods=['GET'])
def get_bot_info_by_id(botid):
    
    bot_info = get_bot_by_id(botid)
    if not bot_info:
        return create_returnable_internal_error_template(InternalErrorCode.BotNotExist)
    return jsonify(bot_info[0]), SUCCESS_CODE

@users_bp.route('/bot/update', methods=['PUT'])
@authorization_required
def update_bot():
    return jsonify(request.json), SUCCESS_CODE

@users_bp.route('/bot/remove', methods=['DELETE'])
@authorization_required
def remove_bot():
    userid = get_user_info(request.authorization.token).id
    remove_user_bot(userid)
    return {}, SUCCESS_CODE
    



@users_bp.route('/testing', methods=['GET'])
@authorization_required
def testing():
    action = supabase.from_('tests').insert({'some_data': '1234Hello'})
    action.headers['Authorization'] = 'Bearer ' + request.authorization.token
    print(action.headers.get_list('authorization'))
    # actionjson = action.headers.items()
    # print(actionjson)
    response = action.execute()
    
    return jsonify({}), SUCCESS_CODE
