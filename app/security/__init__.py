from functools import wraps
from flask import jsonify, request
from app.errors.http_error_templates import create_unauthorized_error
from app.services.session_manager import get_supabase_session
from app.extensions import supabase

def authorization_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        access_token = None
        header = request.authorization 
        if header:
            access_token = header.token
            
        if not access_token or 'undefined' in access_token:
            return create_unauthorized_error()

        return f(*args, **kwargs)
    return decorated

