import requests
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import xmltodict
import xml
from app.services.logging_manager import get_logger

logger = get_logger(__name__)

def expand_sitemap_index(index_path):
    """
    Given a path of a sitemap INDEX, extracts the actual SITEMAPS.
    if the INDEX contains other INDEX, then recursively extracts them too.

    Parameters
    ----------
    path : str
        The path of the INDEX

    Returns
    -------
    list
        List of non-INDEX sitemaps.
    """
    sitemap_content = get_and_turn_xml_to_dict(index_path)
    if sitemap_content is None:
        return []
    sm_dicts = sitemap_content['sitemapindex']['sitemap']
    sm_values = [sm['loc'] for sm in sm_dicts]
    expansion = []
    for sitemap in sm_values:
        if get_sitemap_type(sitemap) == 'INDEX':
            logger.info(f'expanding {sitemap}')
            expansion += expand_sitemap_index(sitemap)
        else:
            logger.info(f'added {sitemap}')
            expansion += [sitemap]
    return expansion


def get_and_turn_xml_to_dict(path):
    """
    Gets the xml from a URL and parses it to dict.
    If the data in URL is not XML-parseable then it returns None
    
    Parameters
    ----------
    path : str
        The URL at which the XML is located
    
    Returns
    -------
    dict or None
    """
    sitemap_xml = requests.get(path).text
    try:
        sitemap_dict = xmltodict.parse(sitemap_xml)
        return sitemap_dict
    except xml.parsers.expat.ExpatError:
        logger.error(f"ERROR OCCURED TRYING TO PARSE {path}")
        return None


def mine_pages_form_sitemap(sitemap_paths):
    """
    From the list of non-INDEX sitemaps, extracts the page URLs.
    """
    sites_reached = []
    for sitemap in sitemap_paths:
        sitemap_dict = get_and_turn_xml_to_dict(sitemap)
        if not sitemap_dict:
            continue
        pages = sitemap_dict['urlset']['url']
        if type(pages) == list:
            sites_reached += [page['loc'] for page in pages]
        else:
            sites_reached += [pages['loc']]
    return sites_reached


def get_sitemap_type(path, expensive=True):
    """
    Identifies the type of the sitemap.
    The type can be either INDEX, SITEMAP or None.
    If crucial is selected, then time-expensive method is employed
    regardless of the value of 'expensive' attribute.
    """

    if expensive:
        # THE EXPENSIVE WAY
        xml = get_and_turn_xml_to_dict(path)
        if not xml:
            return None
        if 'sitemapindex' in xml:
            return "INDEX"
        elif 'urlset' in xml:
            return "SITEMAP"
        return None
    else:
        # THE CHEAP WAY
        if 'index' in path:
            return "INDEX"
        else:
            return "SITEMAP"


def fetch_all_sitemap_paths(robots_results):
    """
    Given robots.txt sitemaps, finds all the non-INDEX sitemaps.
    
    Parameters
    ----------
    robots_results : list[str]
        The list of sitemaps extracted from robots.txt
    

    Returns
    -------
    all_paths : list[str]
        List of all the non-INDEX sitemaps.
    """

    all_paths = []
    for path in robots_results:
        path_type = get_sitemap_type(path)
        if path_type == 'INDEX':
            all_paths += expand_sitemap_index(path)
        elif path_type == 'SITEMAP':
            all_paths += [path]
        else:
            continue
    return all_paths


def get_robots_results(base_url):
    """
    Based on base url finds all the given sitemap(s) from robots.txt.
    Returns None if no robots.txt or sitemap.xml exists.

    Parameters
    ----------
    base_url : str
        URL of the website (netloc)

    Returns
    -------
    sitemaps : list[str] or None
        Sitemap(s) listed on robots.txt
        None if no robots.txt or sitemap exists.
    """

    url_robots = urljoin(base_url, 'robots.txt')
    rp = RobotFileParser()
    rp.set_url(url_robots)
    rp.read()
    sitemaps = rp.site_maps()
    return sitemaps
