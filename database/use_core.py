""""
Table objects represents all of the database tables.
The Table is constructed either directly by using 

* the Table constructor, or indirectly by using 
* ORM Mapped classes.

MetaData object: a collection to place tables. A facade around a Python
dictionary that stores a series of Table objects keyed to their string name.

Table: represents a database table and assigns itself to a MetaData collection.

Column: represents a column in a database table, and assigns itself to a Table object.
The collection of Column objects in the parent Table are typically accessed via an
associated array at Table.c
"""

from sqlalchemy import (
    MetaData, 
    Table, 
    Column, 
    Integer, 
    String, 
    ForeignKey, 
    insert, 
    select,
    update,
    delete,
    text, 
    literal_column,
    and_,
    or_,
    func,
    desc,
)
from database.connectivity import engine


metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String)
)
"""
CREATE TABLE user_account (
        id INTEGER NOT NULL,
        name VARCHAR(30),
        fullname VARCHAR,
        PRIMARY KEY (id)
)
"""

print(user_table.c.name)
print(user_table.c.keys())
print(user_table.primary_key)

"""
When foreign key constraint declarations are present, the CREATE statement will containt them.
They are also used to asist constructing SQL expressions.

A ForeighKeyConstraint is typically declared using a column-level notation via the ForeighKey object.

When using the ForeignKye object withint a Column defintion, we can omit the datatype for that Column.
"""

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)
"""
CREATE TABLE address (
        id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        email_address VARCHAR NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES user_account (id)
)
"""

metadata_obj.drop_all(engine)
metadata_obj.create_all(engine)

"""
The create process takes care of emitting CREATE statements in the correct order.
The `drop_all()` will emit DROP statements in the reverse order.
"""

""""
Table Reflection

The process of generating Table and related objects by reading teh current state of a database.
"""

some_table = Table("some_table", metadata_obj, autoload_with=engine)

"""
## Using INSERT

The following `stmt` is an instance of `Insert`.
"""

stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Suqarepants")

print(stmt)

"""
The stringified form is created by producing a Compiled form of the object.
Use `ClauseElement.compile()` to acquire this object.

To view the `name` and `fullname` bound parameters, these are available from
the `Compiled` construct as well.
"""

compiled = stmt.compile()
print(compiled.params)

""""
Invoking the statement can INSERT a row into user_table.
CursorResult.inserted_primary_key returns a tuple because a primary key may contain
multiple columns. It is intended to always contain the complete primary key
of the record just inserted, not just a cursor.lastrowid kind of value.
It is also intended to be populated regardless of whether or not
"autoincrement" were used.
"""

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
    print(result.inserted_primary_key)


"""
If we don't actually use Insert.values() and just print out an empty statement,
we get an insert for every column in the table; if we execute it ranther than
print it, the statement will be compiled to a string based on the parameters passed
to the Connection.execute() method, and only include columns relevant to the
parameters that were passed.
"""

with engine.connect() as conn:
    result = conn.execute(
        insert(user_table),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "patrick", "fullname": "Patrick Start"}
        ]
    )
    conn.commit()


"""
## Using SELECT
"""

stmt = select(user_table).where(user_table.c.name == "spongebob")
print(stmt)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)


"""
The `select()` function accepts positional elements representing any number of

* Column
* Table expressions
* compatible objects

resolved into a list of SQL expressions to be SELECTed from. 
They are returned as columns in the result set.
These elements also serve to create the FROM clause, which is inferred
from columns and table-like expressions passed:
"""

print(select(user_table.c.name, user_table.c.fullname))
print(select(user_table.c["name", "fullname"]))

"""
## Selecting with Textual Column Expressions

The `text()` can be embedded into a Select construct directly.
"""

stmt = select(text("'some phrase'"), user_table.c.name).order_by(user_table.c.name)
with engine.connect() as conn:
    print(conn.execute(stmt).all())


stmt = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(user_table.c.name)
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(f"{row.p}, {row.name}")


"""
## The WHERE 

Use standard Python operators in conjunction with Column and similar objects to generate the
WHERE clause.

To product multiple expressions joined by AND, the where() method may be invoked multiple times.

AND and OR confjunctions are both available using the and_() and or_() functions.
"""
print(select(user_table).where(user_table.c.name == "squidward"))
print(
    select(address_table.c.email_address)
    .where(user_table.c.name == "squidward")
    .where(address_table.c.user_id == user_table.c.id)
)
# A single call to where() also accepts multiple expressions with the same effect:
print(
    select(address_table.c.email_address).where(
        user_table.c.name == "squidward",
        address_table.c.user_id == user_table.c.id
    )
)
print(
    select(address_table.c.email_address).where(
        and_(
            or_(user_table.c.name == "squidard", user_table.name == "sandy"),
            address_table.c.user_id == user_table.c.id,
        )
    )
)

""""
## Explicit FROM clauses and JOINS

The FROM clause is usually inferred based on the expressions in the columns clause
as well as other elements of the Select.

If we set a single column from a particular Table in the COLUMNs clause, it puts that
Table in the FROM clause.

If we put columns from two tables, we get a comma-separated FROM clause.
"""
print(select(user_table.c.name, address_table.c.email_address))

"""
Use one of two methods on Select to join these tables:

* Select.join_from(), allows us to indicate the left and right side of the JOIN explicitly
* Select.join(), indicates only the right side of the JOIN, the left hand-size is inferred
"""
print(
    select(user_table.c.name, address_table.c.email_address).join_from(
        user_table, address_table
    )
)

print(
    select(user_table.c.name, address_table.c.email_address).join(address_table)
)

"""
If the FROM clause is not inferred the way we want, use Select.select_from() to add
elements to the FROM clause explicitly.
"""

print(
    select(address_table.c.email_address).select_from(user_table).join(address_table)
)
print(
    select(func.count("*")).select_from(user_table)
)

"""
## Setting the ON clause

ON clause is produced automatically if Table objects include a single 
ForeignKeyConstraint defintion.

If Table does not have such construct, or there are multiple constraints
in place, we need to specify the ON clause directly.
"""

print(
    select(address_table.c.email_address)
    .select_from(user_table)
    .join(address_table, user_table.c.id == address_table.c.user_id)
)

""""
## ORDER BY

ColumnElement.asc()
ColumnElement.desc()
"""
print(
    select(user_table).order_by(user_table.c.name.desc())
)

"""
## GROUP BY / HAVING

`func` is a special constructor object which will create new instances of
Function when given the name of the a particular SQL function.
"""
print(func.count(user_table.c.id))
print(
    select(user_table.c.name, func.count(address_table.c.id).label("count"))
    .join(address_table)
    .group_by(user_table.c.name)
    .having(func.count(address_table.c.id) > 1)
)
print(
    select(address_table.c.user_id, func.count(address_table.c.id).label("num_addresses"))
    .group_by("user_id")
    .order_by("user_id", desc("num_addresses"))
)

"""
## Using Aliases

Alias construct is constructed using the FromClause.alias() method.
"""

"""
## Subqueries and CTEs

The Subuquery object behaves like any other FROM objet such as a Table.
It includes a Subuquery.c namespace of the columns which it selects.
"""
subq = (
    select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
    .group_by(address_table.c.user_id)
    .subquery()
)

print(subq)
print(select(subq.c.user_id, subq.c.count))

stmt = select(
    user_table.c.name, user_table.c.fullname, subq.c.count
).join_from(
    user_table, subq
)

print(stmt)

"""
## Common Table Expressions
"""

"""
## EXISTS subqueries
"""

subq = (
    select(address_table.c.id).where(user_table.c.id == address_table.c.user_id)
).exists()

print(select(user_table.c.name).where(~subq))


"""
## The update() SQL Expression Construct

The Update.values() method controls the contents of the SET elements of the UPDATE
statement. Parameters can normally be passed using names as keyword arguments.
"""
print(
    update(user_table)
    .where(user_table.c.name == "patrick")
    .values(fullname="Patrick the Star")
)

print(
    update(user_table)
    .values(fullname="Username: " + user_table.c.name)
)

"""
## The delete() Expression Construct
"""
print(
    delete(user_table)
    .where(user_table.c.name == "patrick")
)

"""
Getting Affected Row Count from UPDATE, DELETE
"""
with engine.begin() as conn:
    result = conn.execute(
        update(user_table)
        .value(fullname="Patrick McStar")
        .where(user_table.c.name == "patrick")
    )
    print(result.rowcount)