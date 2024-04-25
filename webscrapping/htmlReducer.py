from bs4 import BeautifulSoup
import re

def process_html(raw_html: str,
                 remove_scripts_and_style: bool = True,
                 focus_body: bool = True):

    soup = BeautifulSoup(raw_html, 'html.parser')

    if remove_scripts_and_style:
        for element in soup(['scripts', 'style']):
            element.decompose()
    target = soup
    if focus_body:
        target = soup.find('body')

    return target.text


def fix_whitespaces(html):
    cleaned = html.replace('\n', ' ')
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned
