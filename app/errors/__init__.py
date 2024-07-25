from flask import Flask
from app.errors.flask_error_handling import handle_exception, handle_not_found, handle_method_not_allowed

def register_errors(app: Flask):
    app.register_error_handler(Exception, handle_exception)
    app.register_error_handler(500, handle_exception)
    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(405, handle_method_not_allowed)