from functools import wraps
from flask import jsonify
from app.errors.http_error_templates import create_unauthorized_error
from app.services.session_manager import get_supabase_session

def authorization_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        session = get_supabase_session()
        if not session:
            return create_unauthorized_error()
        return f(*args, **kwargs)
    return decorated

