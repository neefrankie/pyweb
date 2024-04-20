import json
from typing import Any, Optional
from datetime import datetime, timezone
from uuid import uuid4
import bcrypt
from faker import Faker

from sqlalchemy import Dialect, Engine, String, Text, Boolean, select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
import sqlalchemy.types as types
from marshmallow import Schema, fields

from engines import mysql_engine

def utc_now():
    return datetime.now(timezone.utc)

# Customize datatime in/out of database.
# Similar to Go's Scan and Value interface.
class UTCDateTime(types.TypeDecorator):
    impl = types.DateTime

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any:
        return value
    
    def process_result_value(self, value: Any | None, dialect: Dialect) -> Any | None:
        return value.replace(tzinfo=timezone.utc)

class CustomerSchema(Schema):
    id = fields.Str()
    mobile = fields.Str()
    wechat_id = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()
    update_at = fields.DateTime()

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customer"

    @classmethod
    def from_email(cls, email: str, password: str):
        now = utc_now()
        return cls(
            id=uuid4().hex,
            created_at=now,
            updated_at=now
        ).withCredentials(email, password)

    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True,
    )
    mobile: Mapped[Optional[str]] = mapped_column(
        String(32),
        unique=True,
        nullable=True
    )
    wechat_id: Mapped[Optional[str]] = mapped_column(
        String(256),
        unique=True,
        nullable=True,
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(30),
        unique=True,
        nullable=True,
    )
    password: Mapped[Optional[str]] = mapped_column(
        Text(),
        nullable=True,
    )
    email_verified: Mapped[bool] = mapped_column(
        Boolean(), 
        default=False
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(
        UTCDateTime(),
        nullable=True,
    )
    updated_at: Mapped[Optional[datetime]]
    deleted_at: Mapped[Optional[datetime]]

    def withCredentials(self, email: str, pw: str):
        bytes = pw.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)

        self.email = email
        self.password = hash.decode('utf-8')
        
        return self

    def is_password_matched(self, pw: str) -> bool:
        bytes = pw.encode('utf-8')
        result = bcrypt.checkpw(bytes, self.password.encode('utf-8'))
        return result


def show_customer_ddl():
    print(CreateTable(Customer.__table__))


def verify_password_matched():
    c = Customer().withCredentials('a@b.c', '123456')
    print(c.password)
    ok = c.is_password_matched('123456')
    print(ok)


def rand_customer():
    fake = Faker()
    return Customer.from_email(fake.email(), fake.password())


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable

    show_customer_ddl()
    verify_password_matched()

    engine = mysql_engine()
    
    # create_tables(engine)
    c = rand_customer()

    with Session(engine) as session:
        session.add(c)
        session.commit()
        retrieved = session.scalar(select(Customer).where(Customer.id == c.id))
        print('customer retrieved: ', retrieved)
        print(retrieved.created_at, retrieved.created_at.tzinfo)
        print(retrieved.updated_at)
        
        schema = CustomerSchema()
        result = schema.dumps(c)
        print(result)






    

    
