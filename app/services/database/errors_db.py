from app.extensions import supabase
from flask import request
import traceback

def archive_error(code:int, title:str, error: Exception):
    error_trace = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    response = supabase.from_('internal_errors').insert(
        {
            "code" : code,
            "title" : title,
            "message" : str(error),
            "detail" : error_trace,
            "requester_ip" : request.remote_addr
        }
    ).execute()
    return response
    