from logging.config import dictConfig

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from src import KBPumNamespace, rest, jwt

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s %(levelname)s] %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config['SECRET_KEY'] = '@leXeyZav@R!!_!!-+!.!Ap!*'
app.config['JWT_SECRET_KEY'] = '@leXeyZav1@R!!_!!-+!.!Ap!*2'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 9600000
app.config['JWT_TOKEN_LOCATION'] = ['query_string', 'headers']

CORS(app)
jwt.init_app(app)

app.register_blueprint(rest)

socketio = SocketIO(app, cors_allowed_origins="*")

socketio.on_namespace(KBPumNamespace(app))

if __name__ == '__main__':
    socketio.run(app, port=3001)
