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
    response = supabase.auth.exchange_code_for_session({"auth_code": code})
    return response.session,response.user

def get_logged_in_user_info():
    session = get_session()
    if not session:
        return None
    else:
        return session.user

def get_session():
    return supabase.auth.get_session()

def supabase_session_end():
    supabase.auth.sign_out({"scope": 'local'})
    