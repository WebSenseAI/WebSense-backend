from app import create_app
from dotenv import load_dotenv
load_dotenv()

CONFIG = 'development'

socket, app = create_app(CONFIG)

if __name__ == '__main__':
    socket.run(app, debug=True)