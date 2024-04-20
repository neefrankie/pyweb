# ORM Mapped Class Configuration

## Overview

Two styles of mapper configuration.

A user-defined class that has a `Mapper` configured against a `Table` object.

The class includes behaviors linked to relational operations both at the class adn instance level.

* imperative mapping
* declarative mapping

All ORM mappings originate from a single object known as `registry`, which is a registry of mapped classes.

### Declarative Mapping

1. Construct a base class using the `DeclarativeBase`.
2. Inherit this base class.

The resulting base class will apply the declarative mapping process to all subclasses that derive from it, relative to a particular `registry` that is local to the new base by default.

The base calss refers to:

* a `registry` object that maitains a collection of related mapped classes
* a `MetaData` object that retains a collection of `Table` objects

## Mapping Classes with Declarative

### Declarative Mapping Styles

* Using a Declarative Base Class
* Using a Decorator

#### Using a Declarative Base Class

```py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclaractiveBase):
    pass

class User(Base):
    __tablename__ = "tablename"

    id = mapped_column(Integer, primary_key=True)

```

#### Using a Decorator

The `registry.mapped()` function is a class decarator that can be applied to any Python class with no hierarchy in place.

```py
mapper_registry = registry()

@mapper_registry.mapped
class User:
    __tablename__ = "user"
```

The mapping of a particular class will only proceed if the decorator is applied to that class directly. The decorator should be applied to each subclass that is to be mapped.

```py
@mapper_registry.mapped
class Person:
    __tablename__ = "person"

@mapper_registry.mapped
class Employee(Person):
    __tablename__ = "employee"
```

### Table Configuration with Declarative

The body of the mapped class includes an attribute `__tablename__`. This is the name of a `Table`.

The `mapped_column()` is used within the class body as class level attributes to indicate columns in the table.

`__name` arg indicates the name of the column. Typically omitted.

`mapped_column()` can derive its column-configuration information from type annotations. These type annotations must be present within a special SQLAlchemy type called `Mapped`.

```py
id: Mapped[int] = mapped_column(primary_key=True)
```

Declarative will generate an empty `mapped_column()` directive implicitly, whenever a `Mapped` type annotation is encountered that does not have a value assigned to the attribute.

The two qualities that `mapped_column()` derives are:

* datatype
* nullability.

The `mapped_column()` will indicates its column as `NULL` or `NOT NULL` first and foremost by the presence of the `nullable` parameter. If `primary_key` parameter is present and set to `True`, that will also imply that the column should be `NOT NULL`.

In the absence of both, `typing.Opitonal[]` within the `Mapped` type annotation will be used to determine nullability. `typing.Optional[]` means `NULL`, and the absense of `typing.Optional[]` means `NOT NULL`.

If there is no `Mapped[]`, and no `nullable` or `primary_key` parameters, then the default for `Column` is `NULL`.

The nullability of `mapped_column()` could be different from that implied by the annotation. The `nullable` parameter will always take precedence:

```py
data: Mapped[Optional[str]] = mapped_column(nullable=False)
```

will be `STRING NOT NULL`, but can be `None` in Python.

```py
data: Mapped[str] = mapped_column(nullable=True)
```

will be `STRING NULL`, but type checker will no expect the attribute to be `None`.

#### Customizing the Type Map

```py
class Base(DeclarativeBase):
    type_annotation_map = {
        int: BIGINT,
        datetime.datetime: TIMESTAMP(timezone=True),
        str: String().with_variant(NVARCHAR, "mssql")
    }

class SomeClass(Base):
    __tablename__ = "some_table"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.datetime]
    status: Mapped[str]
```

`with_variant()` builds up a type map that's customized to different backends.

#### Mapping Mutlipe Type Configurations to Python Types

```py
# Only used by typing tools
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
```

### Mapper Configuration with Declarative

### Composing Mapped Hierarchies with Mixins

## Integration with databaseses and attrs

## SQL Expressions as Mapped Attributes
