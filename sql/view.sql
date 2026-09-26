
CREATE OR REPLACE VIEW vw_resumo_dispositivo AS
SELECT
    room_id,
    location                         AS device_id,
    COUNT(*)                         AS total_leituras,
    ROUND(AVG(temperature), 2)       AS temp_media,
    MIN(temperature)                 AS temp_min,
    MAX(temperature)                 AS temp_max
FROM temperature_readings
GROUP BY room_id, location
ORDER BY location;

CREATE OR REPLACE VIEW vw_anomalias AS
WITH estatisticas AS (
    SELECT location,
           AVG(temperature)    AS media,
           STDDEV(temperature) AS desvio
    FROM temperature_readings
    GROUP BY location
)
SELECT
    r.reading_id,
    r.location                                  AS ambiente,
    r.noted_date,
    r.temperature                               AS temp,
    ROUND(e.media, 2)                           AS media_ambiente,
    ROUND((r.temperature - e.media) / e.desvio, 2) AS z_score
FROM temperature_readings r
JOIN estatisticas e ON e.location = r.location
WHERE ABS(r.temperature - e.media) > 2 * e.desvio
ORDER BY r.noted_date;

CREATE OR REPLACE VIEW vw_tendencia AS
SELECT
    DATE(noted_date)            AS data_leitura,
    MAX(temperature)            AS temp_max,
    MIN(temperature)            AS temp_min,
    ROUND(AVG(temperature), 2)  AS temp_media,
    COUNT(*)                    AS total_leituras
FROM temperature_readings
GROUP BY DATE(noted_date)
ORDER BY data_leitura;

CREATE OR REPLACE VIEW vw_leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM noted_date)::INT AS hora,
    location                           AS ambiente,
    COUNT(*)                           AS contagem,
    ROUND(AVG(temperature), 2)         AS temp_media
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM noted_date), location
ORDER BY hora, ambiente;
