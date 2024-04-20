import click
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase
from flask import current_app, Flask
from .env import build_mysql_url


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_db():
    engine = create_engine(build_mysql_url(db_name=None), echo=True)
    with current_app.open_resource('schema.sql') as f:
        stmt_table = f.read().decode('utf8')

        with engine.connect() as conn:
            conn.execute(text(stmt_table))
            conn.commit()


# click.command() defines a command line command called
# `init-db` that calls the init_db function and shows
# a success message to the user.
# flask --app flaskr init-db
@click.command('init-db')
def init_db_command():
    """create database"""
    init_db()
    click.echo('Created the database')


def init_table():
    with current_app.app_context():
        db.drop_all()
        db.create_all()


# flask --app flaskr init-table
@click.command('init-table')
def init_table_command():
    init_table()
    click.echo("Initialized the database")


# Register with the application
# The init_db_command functions needs to be registered
# with the application instance.
def init_app(app: Flask):
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_table_command)
    db.init_app(app)
