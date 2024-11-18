import os


class Config:
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    LANG_CHAIN = os.environ.get("LANGCHAIN")
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    CORS_HEADERS = 'Content-Type'
    CORS_RESOURCES = {r"/*": {"origins": "*"}}
    CORS_SUPPORTS_CREDENTIALS = True
    SESSION_TYPE = 'filesystem'
    

class DevelopmentConfig(Config):
    CORS_RESOURCES = {r"/*": {"origins": "http://localhost:5173"}}
    BASE_URL = "http://localhost:5000"

class TestingConfig(Config):
    BASE_URL = "http://localhost:5000"
    CORS_RESOURCES = {r"/*": {"origins": "http://localhost:5173"}}

class ProductionConfig(Config):
    BASE_URL = "https://back.websense-ai.com"
    CORS_RESOURCES = {r"/*": {"origins": "https://app.websense-ai.com"}}

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': Config
}
