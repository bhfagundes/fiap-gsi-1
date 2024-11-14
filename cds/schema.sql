-- Criação das tabelas principais
CREATE TABLE consumo_energia (
    id SERIAL PRIMARY KEY,
    data_registro TIMESTAMP,
    consumo_kwh DECIMAL(10,2),
    tarifa DECIMAL(10,2),
    fonte_energia VARCHAR(50),
    regiao VARCHAR(50)
);

CREATE TABLE metricas_diarias (
    id SERIAL PRIMARY KEY,
    data_registro DATE,
    consumo_medio DECIMAL(10,2),
    pico_consumo DECIMAL(10,2),
    economia_estimada DECIMAL(10,2)
);