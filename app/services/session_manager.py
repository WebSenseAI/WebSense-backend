from flask import session
from app.services.supabase_client_utils import get_session

def get_tokens():
    return {
        "access_token" : session.get('supabase_access_token'),
        "refresh_token" : session.get('supabase_refresh_token')}

def get_flask_session():
    return session

def get_supabase_session():
    return get_session()
