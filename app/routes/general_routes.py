from flask import Blueprint, render_template, request, jsonify, redirect
from app.constants.http_status_codes  import SUCCESS_CODE, UNAUTHORIZED_CODE
from app.errors.http_error_templates import create_unauthorized_error
from app.services.session_manager import get_supabase_session, get_tokens


general_bp = Blueprint('general_bp', __name__)

@general_bp.route('/', methods=['GET'])
def index():
    if not get_supabase_session():
        return render_template('admin_templates/login.html')
    
    return redirect('/home')
        

@general_bp.route('/home')
def welcome():
    if get_supabase_session():
        tokens = get_tokens()
        return render_template('user_templates/user_information.html',
                                access_token=tokens['access_token'],
                                refresh_token=tokens['refresh_token'])
    else:
        return create_unauthorized_error()


@general_bp.route('/check_session')
def check_session():
    session = get_supabase_session()
    return jsonify(session.model_dump()), SUCCESS_CODE