from typing import Optional

from pathlib import Path
from dotenv import dotenv_values
from sqlalchemy import URL

env = dotenv_values(Path.home() / "config/.env")

def build_mysql_url(db_name: Optional[str]= "alchemy") -> URL:
    return URL.create(
        "mysql+pymysql",
        username=env["MYSQL_USER"],
        password=env["MYSQL_PASS"],
        host=env["MYSQL_HOST"],
        port=env["MYSQL_PORT"],
        database=db_name
    )
