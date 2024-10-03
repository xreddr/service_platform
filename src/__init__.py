from flask import Flask
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        LITE_DB='default.sqlite',
        DEFAULT_USER='admin',
        DEFAULT_PASSWORD='password',
        OPEN_REG=True,
        ADMIN_CODE=1
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
        try:
            # touch instance/config_file.py
            # export APP_CONFIG=config_file.py
            app.config.from_envvar('APP_CONFIG')
        except (RuntimeError, FileNotFoundError):
            pass
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():

        from . import db
        app.register_blueprint(db.bp)
        db.init_app(app)
        from . import web
        app.register_blueprint(web.bp)
        from . import auth
        app.register_blueprint(auth.bp)
        from . import api
        app.register_blueprint(api.bp)

    return app
