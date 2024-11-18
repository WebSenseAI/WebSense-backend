import os
from flask import Flask
from app.config import config_by_name
from app.routes import register_routes
from app.extensions import init_extensions
from app.errors import register_errors


def create_app(config_name:str=None):
    template_folder = os.environ.get('TEMPLATE_FOLDER_LOCATION')
    app = Flask(__name__, template_folder=template_folder)
    config_class = config_by_name.get(config_name, 'development')
    app.config.from_object(config_class)
    app.secret_key = os.urandom(24)
    
    
    init_extensions(app)

    register_routes(app)

    register_errors(app)
    
    return app

    