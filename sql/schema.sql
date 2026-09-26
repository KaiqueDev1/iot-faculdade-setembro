
DROP VIEW IF EXISTS vw_resumo_dispositivo;
DROP VIEW IF EXISTS vw_anomalias;
DROP VIEW IF EXISTS vw_anomalias_temperatura;
DROP VIEW IF EXISTS vw_tendencia;
DROP VIEW IF EXISTS vw_tendencia_diaria;
DROP VIEW IF EXISTS vw_leituras_por_hora;

DROP TABLE IF EXISTS temperature_readings;

CREATE TABLE temperature_readings (
    reading_id   TEXT PRIMARY KEY,
    room_id      TEXT NOT NULL,
    noted_date   TIMESTAMP NOT NULL, 
    temperature  NUMERIC(5,2) NOT NULL, 
    location     VARCHAR(3) NOT NULL 
);

CREATE INDEX idx_readings_date ON temperature_readings (noted_date);
CREATE INDEX idx_readings_location ON temperature_readings (location);
