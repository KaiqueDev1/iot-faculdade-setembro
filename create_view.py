from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:admin@localhost:5432/iot_db")

view_sql = """
CREATE OR REPLACE VIEW vw_resumo_dispositivo AS
SELECT "out/in" AS device_id, AVG(temp) AS temp_media, COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY "out/in";
"""

with engine.connect() as conn:
    conn.execute(text(view_sql))
    conn.commit()

print("View vw_resumo_dispositivo criada com sucesso!")