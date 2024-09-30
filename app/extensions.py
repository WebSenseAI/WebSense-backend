from flask_cors import CORS
from swagger_ui import api_doc
from supabase import create_client
from supabase.client import Client, ClientOptions
import os
import vecs


def create_supabase_client():
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    client =  create_client(url, key, options=ClientOptions(flow_type='pkce'))
    return client

cors: CORS = CORS()

supabase: Client = create_supabase_client()

vx = vecs.create_client(os.environ.get('SUPABASE_DB_STRING'))



def init_extensions(app):
    cors.init_app(app, 
                  resources=app.config['CORS_RESOURCES'],
                  supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'])
    api_doc(app, config_path='../swagger.yaml')