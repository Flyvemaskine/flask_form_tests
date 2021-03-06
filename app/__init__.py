import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from config import Config


login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')
bootstrap = Bootstrap()
photos = UploadSet('photos', IMAGES)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    configure_uploads(app, photos)
    patch_request_class(app)
    login.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('App startup')

    return app

from app import models
