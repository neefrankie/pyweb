import os
import typing as t

from flask import Flask
from flask_bootstrap import Bootstrap5


def create_app(test_config: t.Mapping[str, t.Any] | None = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "tuzhi.db"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import models

    models.db.init_app(app)
    # Adds a new command that can be called with the `flask` command.
    # Usage: flask --app tuzhi init-table
    models.init_table(app)

    Bootstrap5(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import ocr

    app.register_blueprint(ocr.bp)
    app.add_url_rule('/', endpoint='index')

    from . import account
    app.register_blueprint(account.bp)

    return app
