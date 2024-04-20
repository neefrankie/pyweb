from pathlib import Path
from dotenv import dotenv_values

env = dotenv_values(Path.home() / "config/.env")