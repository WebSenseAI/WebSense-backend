from flask import Blueprint, request, jsonify
from app.constants.http_status_codes import SUCCESS_CODE, UNAUTHORIZED_CODE
from app.services.supabase_client_utils import get_logged_in_user_info
from app.services.database.bots_db import create_new_bot
from app.errors.http_error_templates import create_error_template

# Blueprint for user routes

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/userinfo')
def userinfo():
    userinfo = get_logged_in_user_info()
    if userinfo:
        return jsonify(userinfo.model_dump()), SUCCESS_CODE
    else:
        return jsonify(create_error_template(UNAUTHORIZED_CODE,
                                             "Unauthorized",
                                             "No logged in user.")),UNAUTHORIZED_CODE
    
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
