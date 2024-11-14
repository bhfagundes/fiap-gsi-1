CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    state VARCHAR(2)
);

CREATE TABLE aneel_dados (
    id SERIAL PRIMARY KEY,
    region_id INTEGER REFERENCES regions(id),
    data_geracao TIMESTAMP,
    periodo_referencia VARCHAR(7),
    estado VARCHAR(2),
    municipio VARCHAR(100),
    tipo_consumidor VARCHAR(50),
    classe_consumo VARCHAR(50),
    subclasse_consumo VARCHAR(100),
    potencia_instalada_kw DECIMAL(15,2),
    quantidade_uc INTEGER,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    tensao_fornecimento VARCHAR(50),
    grupo_tensao VARCHAR(10),
    situacao_ativacao VARCHAR(50),
    data_conexao DATE,
    data_ativacao DATE,
    fonte_energia VARCHAR(100),
    modalidade_tarifaria VARCHAR(100),
    grupo_tarifario VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE metricas_diarias (
    id SERIAL PRIMARY KEY,
    region_id INTEGER REFERENCES regions(id),
    data_registro DATE,
    consumo_medio DECIMAL(10,2),
    pico_consumo DECIMAL(10,2),
    economia_estimada DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50),
    timestamp TIMESTAMP,
    light_level INTEGER,
    distance FLOAT,
    internal_led BOOLEAN,
    external_led BOOLEAN,
    energy_saved_kwh DECIMAL(10,4)
);

CREATE INDEX idx_aneel_data_geracao ON aneel_dados(data_geracao);
CREATE INDEX idx_aneel_region ON aneel_dados(region_id);
CREATE INDEX idx_aneel_estado ON aneel_dados(estado);
CREATE INDEX idx_metricas_data ON metricas_diarias(data_registro);
CREATE INDEX idx_sensor_timestamp ON sensor_readings(timestamp);