from flask import Flask
from app.routes.user_routes import users_bp
from app.routes.admin_routes import admins_bp
from app.routes.general_routes import general_bp
from app.routes.auth_routes import auth_bp
from app.routes.chat_routes import chat_bp

def register_routes(app: Flask):
    app.register_blueprint(users_bp,url_prefix='/api')
    app.register_blueprint(admins_bp,url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(general_bp)
