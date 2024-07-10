from flask import Blueprint, render_template, request, jsonify, redirect
from app.constants.http_status_codes  import SUCCESS_CODE, UNAUTHORIZED_CODE
from app.errors.http_error_templates import create_error_template
from app.services.session_manager import does_session_exist, get_supabase_session_data


general_bp = Blueprint('general_bp', __name__)

@general_bp.route('/', methods=['GET'])
def index():
    if not does_session_exist():
        return render_template('admin_templates/login.html')
    return redirect('/home')
        

@general_bp.route('/home')
def welcome():
    if does_session_exist():
        at, rt = get_supabase_session_data()
        return render_template('user_templates/user_information.html',access_token=at, refresh_token=rt)
    else:
        return jsonify(create_error_template(UNAUTHORIZED_CODE,
                "Unauthorized", "The user is not authorized")), UNAUTHORIZED_CODE
