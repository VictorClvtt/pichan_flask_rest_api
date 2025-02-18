import os

from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from db import db

# Importing routes, classes and methods from ./resources
from resources.board_group import blp as BoardGroupBlueprint
from resources.board import blp as BoardBlueprint
from resources.thread import blp as ThreadBlueprint
from resources.reply import blp as ReplyBlueprint
from resources.image import blp as ImageBlueprint
from resources.vote import blp as VoteBlueprint

from resources.jinja2.index import blp as IndexBlueprint

from resources.jinja2.admin import blp as AdminBlueprint

from resources.fingerprint import blp as FingerprintBlueprint

def create_app(db_url=None):

    app = Flask(__name__)
    CORS(app)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'PiChan REST API'
    app.config['API_VERSION'] = 'v1'

    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    # SQLAlchemy configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', f'sqlite:///{os.path.abspath("data.db")}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    # Registering the routes, classes and methods defined in the ./resources folder
    api.register_blueprint(BoardGroupBlueprint)
    api.register_blueprint(BoardBlueprint)
    api.register_blueprint(ThreadBlueprint)
    api.register_blueprint(ReplyBlueprint)
    api.register_blueprint(ImageBlueprint)
    api.register_blueprint(VoteBlueprint)

    api.register_blueprint(IndexBlueprint)

    api.register_blueprint(AdminBlueprint)

    api.register_blueprint(FingerprintBlueprint)

    return app
