from bs4 import BeautifulSoup
import re
from flask_socketio import emit

def process_html(raw_html: str,
                 remove_scripts_and_style: bool = True,
                 focus_body: bool = True,
                 socketio = None):
    """
    Processes html, removes tags, preserves the textual content.
    Parameters
    ----------
    raw_html : str
        The raw HTML to be processed
    remove_scripts_and_style : bool, optional
        Removes `<script>` and `<style>` tags (Default: True)
    focus_body : bool, optional
        Focuses only on the content of `<body>` tag (Default: True)
    """

    
    soup = BeautifulSoup(raw_html, 'html.parser')

    if remove_scripts_and_style:
        for element in soup(['scripts', 'style']):
            element.decompose()
    
    target = soup

    title = soup.find('title')
    if title is not None and socketio is not None:
        socketio.emit('message', {'data': title.text})

    if focus_body:
        body = soup.find('body')
        if body is not None:
            target = body
        else:
            print('No <body> tag found. Processing the whole HTML')
            return None

    return target.text


def fix_whitespaces(html):
    """
    Fixes consecutive whitespaces and new lines (`\\n`)
    
    Parameters
    ----------
    html : str
        The text that will be fixed
    """
    if html is None:
        print("No HTML to process")
        return None
    # Convert all new lines into spaces
    cleaned = html.replace('\n', ' ')
    # Reduce consecutive whitepsaces to a single one
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned