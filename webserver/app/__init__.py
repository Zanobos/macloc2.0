import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(path="api/socket.io")

def create_app(config_class=Config):

    app = Flask(__name__, static_url_path=config_class.STATIC_URL_PATH)

    config_log(app)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    socketio.init_app(app)
    return app

def config_log(app):
    handler = RotatingFileHandler(filename='logs/webserver.log', 
                                  maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
