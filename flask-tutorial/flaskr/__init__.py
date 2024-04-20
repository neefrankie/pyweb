import os
from flask import Flask
from flask_bootstrap import Bootstrap5

from .env import build_mysql_url


# Run the app:
# flask --app flaskr run --debug
def create_app(test_config=None):
    # __name__ is the name of the current Python module.
    # The app needs to know where it's located to set up some paths,
    # and __name__ is a convenient way to tell it that.
    # instance_relative_config tells teh app that configuration files are relative
    # to the instance folder.
    # The instance folder is located outside the flaskr package and can hold
    # local data that shouldn't be committed to version control, such as
    # configuration secrets and the database file.
    app = Flask(__name__, instance_relative_config=True)
    # Sets some default configuration that the app will use:
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=build_mysql_url(),
        SQLALCHEMY_ECHO=True,
    )

    if test_config is None:
        # load the instance config, if it exists, when no testing
        # Override the default configuration with values taken from the config.py
        # file with values taken from the config.py file in the instance folder
        # if it exists.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in.
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    Bootstrap5(app)

    # Import and register the blueprint using app.register_blueprint().
    from . import auth
    app.register_blueprint(auth.bp)

    from . import ocr

    app.register_blueprint(ocr.bp)
    app.add_url_rule('/', endpoint='index')

    from . import account
    app.register_blueprint(account.bp)

    return app

