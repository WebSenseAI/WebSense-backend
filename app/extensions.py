from flask_cors import CORS
from swagger_ui import api_doc
from supabase import create_client
from supabase.client import Client, ClientOptions
import geoip2.database
from geoip2.database import Reader
import os
import vecs
import requests
import tarfile

def create_supabase_client():
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    client =  create_client(url, key, options=ClientOptions(flow_type='pkce'))
    return client

def download_geodatabase():
    base_path = os.environ.get('GEOIP_DB_PATH')
    db_path = os.path.join(base_path,'GeoLite2-Country.mmdb')
    tar_path = os.path.join(base_path,'GeoLite2-Country.tar.gz')
    
    
    licence_key= os.environ.get('GEOIP_LICENCE_KEY')
    download_path = f'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key={licence_key}&suffix=tar.gz'
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path),exist_ok=True)
        response = requests.get(download_path, stream=True)
        if response.status_code == 200:
            with open(tar_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print('Database tar download is successfull')
            
            with tarfile.open(tar_path, 'r:gz') as tar:
                for member in tar.getmembers():
                    if member.name.endswith('.mmdb'):
                        member.name = os.path.basename(member.name)
                        tar.extract(member, base_path)
                        break
            print('Tar extraction succesfull')
            os.remove(tar_path)
            print('Database setup successfull')
        else:
            print('Failed to download geolite2 country database')

def load_geocountry_db():
    download_geodatabase()
    path = os.path.join(os.environ.get('GEOIP_DB_PATH'), 'GeoLite2-Country.mmdb') 
    return geoip2.database.Reader(path)

cors: CORS = CORS()

supabase: Client = create_supabase_client()

vx = vecs.create_client(os.environ.get('SUPABASE_DB_STRING'))

geoip_reader: Reader = load_geocountry_db()

def init_extensions(app):
    cors.init_app(app, 
                  resources=app.config['CORS_RESOURCES'],
                  supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'])
    api_doc(app, config_path='../swagger.yaml')

