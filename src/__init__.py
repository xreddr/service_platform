from flask import Flask, session
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev'
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

        from . import web
        app.register_blueprint(web.bp)
        from . import db
        app.register_blueprint(db.bp)
        # db.ping_conn()
        from . import auth
        app.register_blueprint(auth.bp)
        from . import api
        app.register_blueprint(api.bp)

    return app
