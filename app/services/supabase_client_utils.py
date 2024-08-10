import base64
import hashlib
from app.extensions import supabase

def generate_code_challenge(code_verifier: str) -> str:
    # Generate the code challenge from the code verifier
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip('=')
    return code_challenge

def get_oauth_provider_url(provider: str, redirect_url: str, code_verifier: str) -> str:
    # Generate the code challenge
    code_challenge = generate_code_challenge(code_verifier)

    # Construct the OAuth URL with PKCE parameters
    oauth_url = supabase.auth.get_oauth_url(
        provider=provider,
        redirect_url=redirect_url,
        code_challenge=code_challenge,
        code_challenge_method="S256"  # Ensure this method is supported
    )
    return oauth_url

def exchange_with_session(code:str):
    response = supabase.auth.exchange_code_for_session({"auth_code": code})
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
    