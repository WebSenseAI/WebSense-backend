from flask import Blueprint, jsonify, request, redirect, current_app, session
from app.constants.http_status_codes import SUCCESS_CODE, BAD_REQUEST_CODE
from app.errors.http_error_templates import create_returnable_internal_error_template
from app.services.supabase_client_utils import get_oauth_provider_url, exchange_with_session, supabase_session_end
from app.services.database.users_db import create_internal_user_with_supabase_code
from app.extensions import supabase
from app.constants.internal_errors import InternalErrorCode
import os

auth_bp = Blueprint('auth_bp', __name__)


####### DEPRECIATED #########
# THE CODE IN THIS FILE IS FROM THE OLDER METHOD
# IN THE NEW METHOD, THE AUTHORIZATION IS DONE IN THE FRONT END


@auth_bp.route('/oauth/callback', methods=['GET'])
def callback_post_google():
    code = request.args.get("code")
    sb_session, user = exchange_with_session(code)
    create_internal_user_with_supabase_code(user)
    session['supabase_access_token'] = sb_session.access_token
    session['supabase_refresh_token'] = sb_session.refresh_token
    return redirect('https://websense-frontend.up.railway.app')


@auth_bp.route('/register/oauth/<provider>', methods=['GET'])
def continue_with_provider(provider: str):
    available_providers = os.environ.get("SUPPORTED_PROVIDERS").split(',')
    if provider not in available_providers:
        return create_returnable_internal_error_template(InternalErrorCode.InvalidProvider)

    base_url = current_app.config['BASE_URL']
    redirect_url = f"{base_url}/auth/oauth/callback"

    oauth_url = get_oauth_provider_url(provider=provider,
                                       redirect_url=redirect_url)

    return redirect(oauth_url)


@auth_bp.route('/logout', methods=['GET'])
def logout():
    supabase_session_end()
    return {}, SUCCESS_CODE