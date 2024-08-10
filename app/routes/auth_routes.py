from flask import Blueprint, jsonify, request, redirect, current_app, session
from flask_cors import cross_origin
from app.constants.http_status_codes import SUCCESS_CODE, BAD_REQUEST_CODE
from app.errors.http_error_templates import create_returnable_internal_error_template
from app.services.supabase_client_utils import get_oauth_provider_url, exchange_with_session, supabase_session_end
from app.services.database.users_db import create_internal_user_with_supabase_code
from app.extensions import supabase
from app.constants.internal_errors import InternalErrorCode
import os

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/oauth/callback<code>', methods=['GET','POST'])
@cross_origin()
def callback_post_google(code:str):
    if not code:
        return jsonify({'error': 'Authorization code missing'}), BAD_REQUEST_CODE

    code_verifier = session.get('code_verifier')
    if not code_verifier:
        return jsonify({'error': 'Code verifier missing'}), BAD_REQUEST_CODE

    try:
        # Exchange the authorization code and code verifier for tokens
        sb_session, user = exchange_with_session(code, code_verifier)
        if not sb_session or not sb_session.access_token:
            return jsonify({'error': 'Failed to retrieve access token'}), BAD_REQUEST_CODE
        
        create_internal_user_with_supabase_code(user)
        
        access_token = sb_session.access_token
        session['supabase_access_token'] = access_token
        session['supabase_refresh_token'] = sb_session.refresh_token
        
        return redirect(f'https://websense-frontend.up.railway.app/?access_token={access_token}')
    except Exception as e:
        return jsonify({'error': str(e)}), BAD_REQUEST_CODE
    
    
@auth_bp.route('/register/oauth/<provider>', methods=['GET'])
@cross_origin()
def login_with_provider(provider: str):
    available_providers = os.environ.get("SUPPORTED_PROVIDERS", "").split(',')
    if provider not in available_providers:
        return jsonify({'error': 'Invalid provider'}), BAD_REQUEST_CODE
    base_url = current_app.config['BASE_URL']
    redirect_url = f"{base_url}/auth/oauth/callback"
    try:
        oauth_url = get_oauth_provider_url(provider=provider, redirect_url=redirect_url)
        return jsonify({'url': oauth_url}), SUCCESS_CODE
        #return redirect(oauth_url)
    except Exception as e:
        return jsonify({'error': str(e)}), BAD_REQUEST_CODE

@auth_bp.route('/logout', methods=['GET'])
def logout():
    try:
        supabase_session_end()
        session.pop('supabase_access_token', None)
        session.pop('supabase_refresh_token', None)
        return {}, SUCCESS_CODE
    except Exception as e:
        return jsonify({'error': str(e)}), BAD_REQUEST_CODE


@auth_bp.route('/status/<supabase_access_token>', methods=['GET'])
def check_auth_status(supabase_access_token: str):
    access_token = supabase_access_token
    if not access_token:
        return jsonify({'authenticated': False}), InternalErrorCode.BotNotExist
    try:
        is_valid = verify_token(access_token)
        return jsonify({'authenticated': is_valid}), SUCCESS_CODE
    except Exception as e:
        return jsonify({'authenticated': False, 'error': str(e)}), SUCCESS_CODE
    

def verify_token(access_token):
    user = supabase.auth.get_user(access_token)
    return user is not None