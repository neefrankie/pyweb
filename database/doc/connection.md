# Create Engine

This should the 1st step learning SQLAlchemy.

The content is scattered around:

* ORM Quik Start, Create an Engine;
* Establishing  Connectivity - the Engine

Every SQLAlchemy application that connects to a database needs to use an Engine. This object acts as a central souce of connections to a particular database, providing both a factory as well as a connection pool for these database connections.

The engine is typically a global object created just once for a particular database server.

```py
from sqlalchemy import create_engine

engine = create_engine("sqlite:///temp/foo.db", echo=True)
```

The main argument to create_engine is a string URL:

1. What kind of database are we communicating with?

2. What DBAPI are we using? If omitted, SQLAlchemy will use a default DBAPI for the particular database selected.

3. How to locate the database?

The parameter `echo` will instruct the Engine to log all of the SQL emitted to standard out.

Primary interactive endpoint of an Engine:

* Connection: represents an open resouece against the database.
* Result

## Engine Configuration

The Engine can be used either to directly interact with the databae, or can be passed to a `Session` object to work with the ORM.

## Database URLs

Typical form of a database URL:

```py
dialect+driver://username:password@host:port/database
```

`dialect` could be:

* slite
* mysql
* postgresql
* oracle
* mssql

The driver name is the name of the DBAPI to be used to connect to the database. If not specified, a default DBAPI will be imported if available.

The value passed to `create_engine()` may be an instance of URL instead o a plain string.

The URL object is created using the `URL.create()` constructor method, passing all the fields individually.

## PostgreSQL

Uses psycopg2 as the default DBAPI. Other include:

* pg8000
* asyncpg

```py
url_object = URL.create(
    "postgresql+pg8000",
    username="dbuser",
    password="kx@jj5/g",
    host="pghost10",
    database="appdb"
)

engine = create_engine(url_object)

engine = create_engine("posgresql://scott:tiger@localhost/mydatabase")

engine = create_engine("postgresql+psycopg2://scott:tiger@locahost/mydatabase")

engine = create_engine("postgresql+pg8000://scott:tiger@locahost/mydatabase")
```

## MySQL

Use mysqlclient as the default DBAPI.

```py
engine = create_engine("mysql://scott:tiger@localhost/foo")

engine = create_engine("mysql+mysqldb://scott:tiger@localhost/foo")

engine = create_engine("mysql+pymysql://scott:tiger@localhost/foo")
```

## SQLite

For a relative file path, there are 3 slashes:

`sqlite://<nohostname>/<path>`

```py
engine = create_engine("sqlite:///foo.db")

# For an asbolute file path, the three slashes are followed by the absolute path:

engine = create_engine("sqlite:////absolute/path/to/foo.db")

engine = create_engine("sqlite:///C:\\path\\to\\foo.db")

engine = create_engine(r"sqlite:///C:\path\to\foo.db")

# To use a SQLite `:memory:` database, specify an empty URL

engine = create_engine("sqlite://")
```