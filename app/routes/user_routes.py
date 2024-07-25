from flask import Blueprint, request, jsonify
from app.constants.http_status_codes import SUCCESS_CODE, UNAUTHORIZED_CODE, BAD_REQUEST_CODE
from app.services.supabase_client_utils import get_logged_in_user_info, get_logged_in_user_id
from app.services.database.bots_db import create_new_bot, get_user_bot
from app.errors.http_error_templates import create_unauthorized_error, create_internal_error_template
from app.constants.internal_errors import InternalErrorCode


# Blueprint for user routes

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/userinfo')
def userinfo():
    userinfo = get_logged_in_user_info()
    if userinfo:
        return jsonify(userinfo.model_dump()), SUCCESS_CODE
    else:
        return create_unauthorized_error()
    
@users_bp.route('/bot/new', methods=['POST'])
def create_bot():
    data = request.json
    create_new_bot(
        name = data['name'],
        website_url=data['website'],
        description=data['description'],
        first_message=data['message'],
        openai_key=data['key']
    )
    return {},SUCCESS_CODE


@users_bp.route('/bot/info', methods=['GET'])
def get_bot_info():
    userid = get_logged_in_user_id()
    if not userid:
        return create_unauthorized_error()

    bot_info = get_user_bot(userid)
    if not bot_info:
        return jsonify(create_internal_error_template(InternalErrorCode.BotNotExist)), BAD_REQUEST_CODE
    
    return jsonify(bot_info[0]), SUCCESS_CODE