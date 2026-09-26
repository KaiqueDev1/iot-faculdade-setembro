
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SQL_DIR = BASE_DIR / "sql"

CSV_PATH = DATA_DIR / "temperature_readings.csv"

load_dotenv(BASE_DIR / ".env")


def get_database_url() -> str:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "admin")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "iot_db")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"


def get_engine() -> Engine:
    return create_engine(get_database_url())


def run_sql_file(engine: Engine, filename: str) -> None:
    sql = (SQL_DIR / filename).read_text(encoding="utf-8")
    with engine.begin() as conn:
        conn.exec_driver_sql(sql)
