from flask import Blueprint, request, jsonify
from app.constants.http_status_codes import SUCCESS_CODE
from app.services.supabase_client_utils import get_logged_in_user_info
from app.errors.http_error_templates import create_error_template
from app.constants.http_status_codes import UNAUTHORIZED_CODE

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
