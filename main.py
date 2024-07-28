from app import create_app
from dotenv import load_dotenv
from app.extensions import socketio
load_dotenv()

CONFIG = 'development'

app = create_app(CONFIG)

if __name__ == '__main__':
    socketio.run(app, debug=True)