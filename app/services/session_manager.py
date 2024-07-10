from flask import session

def get_supabase_session_data():
    return session.get('supabase_access_token'),session.get('supabase_refresh_token')

def get_session():
    return session

def does_session_exist():
    at, rt = get_supabase_session_data()
    return at is not None and rt is not None