from app.constants.internal_errors import InternalErrorCode
from app.constants.http_status_codes import UNAUTHORIZED_CODE
from flask import jsonify

def create_error_template(code: int, error: str, message: str):
    return {
        "code": code,
        "error": error,
        "message": message
    }


def create_internal_error_template(error: InternalErrorCode):
    return {
        "code": error.get_code(),
        "error": error.get_description(),
        "message": error.get_message()
    }


def create_unauthorized_error():
    return jsonify(create_error_template(UNAUTHORIZED_CODE,
                                "Unauthorized",
                                "No logged in user.")), UNAUTHORIZED_CODE