from app.extensions import geoip_reader
import geoip2.errors


def get_requester_country(ip_address: str):
    try:
        response = geoip_reader.country(ip_address=ip_address)
        return response.country.iso_code
    except geoip2.errors.AddressNotFoundError:
        return None
    