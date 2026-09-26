import pandas as pd

from config import CSV_PATH, get_engine, run_sql_file

COLUMN_MAP = {
    "id": "reading_id",
    "room_id/id": "room_id",
    "noted_date": "noted_date",
    "temp": "temperature",
    "out/in": "location",
}


def extract() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    print(f"[extract] {len(df)} linhas lidas de {CSV_PATH.name}")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=COLUMN_MAP)[list(COLUMN_MAP.values())]

    df["noted_date"] = pd.to_datetime(df["noted_date"], format="%d-%m-%Y %H:%M")

    antes = len(df)
    df = df.dropna().drop_duplicates(subset="reading_id")
    print(f"[transform] {antes - len(df)} linha(s) removida(s) (nulos/duplicados)")

    return df


def load(df: pd.DataFrame) -> None:
    engine = get_engine()

    run_sql_file(engine, "schema.sql")

    df.to_sql(
        "temperature_readings",
        engine,
        if_exists="append",  
        index=False,
        chunksize=5000,
        method="multi",
    )

    total = pd.read_sql("SELECT COUNT(*) AS total FROM temperature_readings", engine)
    print(f"[load] {int(total['total'][0])} linhas gravadas no PostgreSQL")


if __name__ == "__main__":
    load(transform(extract()))
    print("ETL concluído. Agora execute: python src/create_view.py")
