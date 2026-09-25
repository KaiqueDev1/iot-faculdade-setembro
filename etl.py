import os
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/iot_db"
engine = create_engine(DATABASE_URL)

df = pd.read_csv("data/temperature_readings.csv")
print("Colunas do CSV:", df.columns.tolist())

df.to_sql("temperature_readings", engine, if_exists="replace", index=False)
print("Dados carregados com sucesso no banco de dados.")