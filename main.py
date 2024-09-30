from app import create_app
from dotenv import load_dotenv
load_dotenv()

CONFIG = 'production'

app = create_app(CONFIG)
