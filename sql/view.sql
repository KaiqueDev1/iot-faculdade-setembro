-- View 1: Resumo por dispositivo
CREATE VIEW vw_resumo_dispositivo AS
SELECT device_id, AVG(temperature) as temp_media, COUNT(*) as total_leituras
FROM temperature_readings
GROUP BY device_id;

-- View 2: Leituras fora do padrão (Anomalias)
CREATE VIEW vw_anomalias_temperatura AS
SELECT * 
FROM temperature_readings
WHERE temperature > 40 OR temperature < 0;

-- View 3: Tendência diária
CREATE VIEW vw_tendencia_diaria AS
SELECT DATE(timestamp) as data_leitura, MAX(temperature) as temp_maxima, MIN(temperature) as temp_minima
FROM temperature_readings
GROUP BY DATE(timestamp);