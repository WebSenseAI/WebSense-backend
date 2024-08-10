from flask import session
from app.extensions import supabase

def get_oauth_provider_url(provider:str, redirect_url:str):
    data = supabase.auth.sign_in_with_oauth({
        "provider": provider,
        "options": {
            "redirect_to": redirect_url
            
        }
    })
    return data.url

def exchange_with_session(code:str):
    code_verifier = session.get('code_verifier')

    response = supabase.auth.exchange_code_for_session({"auth_code": code, "code_verifier": code_verifier})
    return response.session,response.user

def get_logged_in_user_info():
    session = get_session()
    if not session:
        return None
    else:
        return session.user

def get_logged_in_user_id():
    user = get_logged_in_user_info()
    return user.id if user else None

def get_session():
    return supabase.auth.get_session()

def supabase_session_end():
    supabase.auth.sign_out({"scope": 'local'})
    