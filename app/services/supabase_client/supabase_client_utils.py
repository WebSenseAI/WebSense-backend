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
