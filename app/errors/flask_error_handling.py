from flask import jsonify
from app.errors.http_error_templates import create_error_template
from app.constants.http_status_codes import INTERNAL_SERVER_ERROR_CODE, NOT_FOUND_CODE, METHOD_NOT_ALLOWED_CODE

def handle_exception(e: Exception):
    template = create_error_template(
        code=INTERNAL_SERVER_ERROR_CODE,
        error="Unknown error occured",
        message=str(e)
    )
    return jsonify(template), INTERNAL_SERVER_ERROR_CODE

def handle_not_found(e):
    template = create_error_template(
        code=NOT_FOUND_CODE,
        error="Not found",
        message="The requested source was not found"
    )
    return jsonify(template), NOT_FOUND_CODE

def handle_method_not_allowed(e):
    template = create_error_template(
        code=METHOD_NOT_ALLOWED_CODE,
        error="Method not allowed",
        message="The HTTP method is not allowed"
    )



    


