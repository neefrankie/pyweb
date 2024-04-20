from sqlalchemy import URL, create_engine, Engine, text
from dotenv import dotenv_values
from pathlib import Path


config = dotenv_values(Path.home() / "config/.env")


# Build a sqlite connection URL.
def build_sqlite_url(path: str="temp/foo.db") -> URL:
    return URL.create(
        "sqlite",
        database=path
    )

# Create sqlite engine.
def sqlite_engine() -> Engine:
    return create_engine(build_sqlite_url(), echo=True)


def build_mysql_url(db_name: str="alchemy") -> URL:
    return URL.create(
        "mysql+pymysql",
        username=config["MYSQL_USER"],
        password=config["MYSQL_PASS"],
        host=config["MYSQL_HOST"],
        port=config["MYSQL_PORT"],
        database=db_name
    )


def mysql_engine() -> Engine:
    return create_engine(build_mysql_url(), echo=True)






def init_mysql():
    engine = create_engine(build_mysql_url(db_name=None), echo=True)
    stmt_table = """
    CREATE DATABASE IF NOT EXISTS alchemy
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;
    """
    with engine.connect() as conn:
        conn.execute(text(stmt_table))
        conn.commit()




if __name__ == "__main__":
    init_mysql()
    