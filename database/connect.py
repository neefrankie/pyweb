from sqlalchemy import text
from engines import mysql_engine

engine = mysql_engine()

"""
## Getting a Connection
"""

with engine.connect() as conn:
    result = conn.execute(text("SELECT 'hello world'"))
    print(result.all())

"""
When the scope of the connection is released, a ROLLBACK is emitted to end the transaction.
The transaction is not committed automatically.

## Committing Changes
"""

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS some_table(x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    conn.commit()

"""
Another style of committing data using transaction block up front.
Use `Engine.begin()` to acquire the connection.
"""

with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )

"""
## Fetching Rows

Result is an iterable object of each rows.

Result.all() reeturns a list of all Row object.

Row acts like Python named tuples.
"""

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x} y: {row.y}")

    for x, y in result:
        print(f"x: {x} y: {y}")

# Tuple assignement
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))

    for x, y in result:
        print(f"x: {x} y: {y}")

"""
Integer index:

for row in result:
    x = row[0]

Mapping access:

for dict_row in result.mappings():
    x = dict_row["x"]
    y = dict_row["y"]


## Sending Parameters

The actual value for `:y` is passed as the second argument to Connection.execute()
in the form of a dictionary.

The bound parameter :y was converted into a question mark when it was sent to the database.
"""

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x} y: {row.y}")


"""
## Sending Multiple Parameters

Send multiple parameter sets to the Connection.execute() method by passing a list of
dictionaries instead of a single dictionary, which indicates that the single SQL
statement should be invoked multiple times, once for each parameter set.

The following is equivalent to running the given INSERT statement once for each
parameter set.
"""

with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [
            {"x": 11, "y": 12},
            {"x": 13, "y": 14}
        ]
    )
    conn.commit()