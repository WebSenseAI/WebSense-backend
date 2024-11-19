from flask_cors import CORS
from swagger_ui import api_doc
from supabase import create_client
from supabase.client import Client, ClientOptions
import geoip2.database
from geoip2.database import Reader
import os
import base64
import requests
import tarfile
from app.services.logging_manager import get_logger

logger = get_logger(__name__)

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
            logger.info('Database tar download is successfull')
            
            with tarfile.open(tar_path, 'r:gz') as tar:
                for member in tar.getmembers():
                    if member.name.endswith('.mmdb'):
                        member.name = os.path.basename(member.name)
                        tar.extract(member, base_path)
                        break
            logger.info('Tar extraction succesfull')
            os.remove(tar_path)
            logger.info('Database setup successfull')
        else:
            logger.error('Failed to download geolite2 country database')

def load_geocountry_db():
    download_geodatabase()
    path = os.path.join(os.environ.get('GEOIP_DB_PATH'), 'GeoLite2-Country.mmdb') 
    return geoip2.database.Reader(path)

def load_db_certificate():
    if os.environ.get("FLASK_ENV", 'production') == 'production':
        cert_base64 = os.environ.get("SUPABASE_SSL_CERT_BASE64")
        if not os.path.exists('./certificates'):
            logger.info('certificates directory does not exist')
            os.mkdir('./certificates')
            logger.info('created certificates directory')
        cert_path = r'./certificates/prod-ca-2021.crt'
        with open(cert_path, 'wb') as cert_file:
            cert_file.write(base64.b64decode(cert_base64))
            logger.info('Successfully created prod-ca-2021')
        logger.info('Verifying certificate')
        if os.path.isfile(cert_path):
            logger.info('Certificate is succesfully located')
        else:
            logger.warning('Certificate not found')   

cors: CORS = CORS()

supabase: Client = create_supabase_client()

load_db_certificate()

geoip_reader: Reader = load_geocountry_db()

def init_extensions(app):
    cors.init_app(app, 
                  resources=app.config['CORS_RESOURCES'],
                  supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'])
    api_doc(app, config_path='../swagger.yaml')
