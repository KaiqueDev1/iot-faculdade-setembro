from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:admin@localhost:5432/iot_db")

sql_queries = [
    """
    CREATE OR REPLACE VIEW vw_resumo_dispositivo AS
    SELECT "out/in" AS device_id, AVG(temp) AS temp_media, COUNT(*) AS total_leituras
    FROM temperature_readings
    GROUP BY "out/in";
    """,
    """
    CREATE OR REPLACE VIEW vw_anomalias AS
    SELECT "out/in" AS ambiente, noted_date, temp
    FROM temperature_readings
    WHERE temp >= 40;
    """,
    """
    CREATE OR REPLACE VIEW vw_tendencia AS
    SELECT SUBSTRING(noted_date, 1, 10) AS data_leitura, MAX(temp) AS temp_max, MIN(temp) AS temp_min
    FROM temperature_readings
    GROUP BY SUBSTRING(noted_date, 1, 10);
    """
]

with engine.connect() as conn:
    for query in sql_queries:
        conn.execute(text(query))
    conn.commit()

print("As 3 Views foram criadas com sucesso no PostgreSQL!")