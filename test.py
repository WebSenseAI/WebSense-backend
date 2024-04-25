import sys, os
cwd = os.getcwd()
sys.path.append(os.path.join(cwd, 'webscrapping'))
from webscrapping.scrapWrapper import trainNewBot

DOMAIN_LUIS = 'luisbeqja.com'

## THIS WILL RETURN A LIST OF PAGES
## IF SAVE=TRUE, THEN CHECK data/extracted/{DOMAIN} TO SEE THE PROCESSED PAGES
trainNewBot(url=DOMAIN_LUIS, save=True)

