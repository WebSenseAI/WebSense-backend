from app.services.webscraping.domainCrawler import Crawler
from app.services.webscraping.htmlReducer import process_html, fix_whitespaces
from app.services.logging_manager import get_logger
import requests
import os

logger = get_logger(__name__)

def trainNewBot(url: str, save: bool = True):
    """
    Wrapper method that is in charge of crawling into a website
    and storing all the meaningful information from its pages.

    The extracted data will be in a form that is ready to be used
    for bot training.

    Parameters
    ----------
    url : str
        The base URL of the site.
    save : bool, optional
        Indicates whether to save the extracted info to local files (Default: False)
    """
    # Add https:// to the url if it is not there.
    url_fixed = ('' if url.startswith('https://') else 'https://') + url
    
    # Crawler object to get page URLs
    crawler = Crawler(url_fixed, expensive=True)
    
    # Initiate crawling
    crawler.crawl()
    
    # save page information
    if save:
        crawler.save()

    # get reached sites
    sites = crawler.get_reached_sites()
    if len(sites) > 100: 
        sites = sites[:100]
        
    extracted_data = []
    # foreach reached url, get their raw HTML, process it and add to the list
    logger.info("Total sites reached:", len(sites))
    for site in sites:
        raw_html = requests.get(site)
        processed = process_html(raw_html=raw_html.text)
        trimmed = fix_whitespaces(html=processed)
        extracted_data.append(trimmed)

    # If save, save the contents
    if save:
        storage_path = fr"data/extracted/{url}"
        if not os.path.isdir('data'):
            os.mkdir('data')
        if not os.path.isdir('data/extracted'):
            os.mkdir('data/extracted')
        
        if os.path.isdir(storage_path):
            os.rmdir(storage_path)

        os.mkdir(storage_path)
        for index, page in enumerate(extracted_data,1):
            if page is not None:
                f_name = f"page_{index}.txt"
                with open(os.path.join(storage_path,f_name), 'w', encoding="utf-8") as f:
                    f.write(page)
            else:
                logger.warning(f"No data to write for page {index}")
    
    return extracted_data