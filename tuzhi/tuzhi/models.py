from typing import (
    List,
    Optional,
)
from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
)
from flask_sqlalchemy import SQLAlchemy
import click
from flask import current_app, Flask


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "user_account"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


def init_db():
    with current_app.app_context():
        db.drop_all()
        db.create_all()


# flask --app tuzhi init-db
@click.command('init-table')
def init_table_command():
    init_db()
    click.echo("Created all tables")


def init_table(app: Flask):
    app.cli.add_command(init_table_command)
