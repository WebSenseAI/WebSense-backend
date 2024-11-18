from app import create_app
from dotenv import load_dotenv
import os
from app.services.logging_manager import get_logger

load_dotenv()

logger = get_logger(__name__)

CONFIG = os.environ.get('FLASK_ENV', 'production')

logger.info(f'Starting the server in \'{CONFIG}\' mode')

app = create_app(CONFIG)

if __name__=="__main__":
    app.run(debug=False)