from app.constants.internal_errors import InternalErrorCode


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