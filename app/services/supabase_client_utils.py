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

def get_user_info(access_token: str):
    return supabase.auth.get_user(access_token).user


# TO BE REVISED
# def get_logged_in_user_id():
#     user = get_logged_in_user_info()
#     return user.id if user else None

def get_session():
    return supabase.auth.get_session()

def supabase_session_end():
    supabase.auth.sign_out({"scope": 'local'})


    