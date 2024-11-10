from app.extensions import geoip_reader
import geoip2.errors
import os
import requests
import tarfile

def get_requester_country(ip_address: str):
    try:
        response = geoip_reader.country(ip_address=ip_address)
        return response.country.iso_code
    except geoip2.errors.AddressNotFoundError:
        return None
    
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