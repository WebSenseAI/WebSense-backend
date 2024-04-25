from webscrapping.domainCrawler import Crawler
from webscrapping.htmlReducer import process_html, fix_whitespaces
import requests
import os

def trainNewBot(url: str, save=False):
    url_fixed = ('' if url.startswith('http://') else 'https://') + url
    print(f"STARTING: {url_fixed}")
    crawler = Crawler(url_fixed, expensive=True)
    crawler.crawl()
    if save:
        crawler.save()

    sites = crawler.get_reached_sites()
    
    extracted_data = []
    for site in sites:
        raw_html = requests.get(site)
        processed = process_html(raw_html=raw_html.text)
        trimmed = fix_whitespaces(html=processed)
        extracted_data.append(trimmed)

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
            f_name = f"page_{index}.txt"
            with open(os.path.join(storage_path,f_name), 'w', encoding="utf-8") as f:
                f.write(page)

    return extracted_data
        
        

        
