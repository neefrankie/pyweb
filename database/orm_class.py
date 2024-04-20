import datetime

from decimal import Decimal

from typing_extensions import Annotated

from sqlalchemy import func
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

"""
## Mapping Multiple Type Configurations to Python Types


"""
str_30 = Annotated[str, 30]
str_50 = Annotated[str, 50]
num_12_4 = Annotated[Decimal, 12]
num_6_2 = Annotated[Decimal, 6]

class Base(DeclarativeBase):
    # mapped_column() only need this.
    registry = registry(
        type_annotation_map={
            str_30: String(30),
            str_50: String(50),
            num_12_4: Numeric(12, 4),
            num_6_2: Numeric(6, 2),
        }
    )

class SomeClass(Base):
    __tablename__ = "some_table"

    short_name: Mapped[str_30] = mapped_column(primary_key=True)
    long_name: Mapped[str_50]
    num_value: Mapped[num_12_4]
    short_num_value: Mapped[num_6_2]

"""
## Mapping Whole Column Declarations to Python Types

Declarative can extract an entire pre-established `mapped_column()` construct from an
Annotated object directly.

The following Annotated object can be used directly within `Mapped`.
"""
intpk = Annotated[int, mapped_column(primary_key=True)]
timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP())
]
required_name = Annotated[str, mapped_column(String(30), nullable=False)]

class SomeClass(Base):
    __tablename__ = "some_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    created_at: Mapped[timestamp]



if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable

    print(CreateTable(SomeClass.__table__))