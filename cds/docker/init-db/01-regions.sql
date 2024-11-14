-- Inserção das regiões e seus estados
INSERT INTO regions (name, state) VALUES
-- Norte
('Norte', NULL),
('Acre', 'AC'),
('Amapá', 'AP'),
('Amazonas', 'AM'),
('Pará', 'PA'),
('Rondônia', 'RO'),
('Roraima', 'RR'),
('Tocantins', 'TO'),

-- Nordeste
('Nordeste', NULL),
('Alagoas', 'AL'),
('Bahia', 'BA'),
('Ceará', 'CE'),
('Maranhão', 'MA'),
('Paraíba', 'PB'),
('Pernambuco', 'PE'),
('Piauí', 'PI'),
('Rio Grande do Norte', 'RN'),
('Sergipe', 'SE'),

-- Centro-Oeste
('Centro-Oeste', NULL),
('Distrito Federal', 'DF'),
('Goiás', 'GO'),
('Mato Grosso', 'MT'),
('Mato Grosso do Sul', 'MS'),

-- Sudeste
('Sudeste', NULL),
('Espírito Santo', 'ES'),
('Minas Gerais', 'MG'),
('Rio de Janeiro', 'RJ'),
('São Paulo', 'SP'),

-- Sul
('Sul', NULL),
('Paraná', 'PR'),
('Rio Grande do Sul', 'RS'),
('Santa Catarina', 'SC')
ON CONFLICT (name) DO NOTHING;

-- Criar índice para otimizar buscas por estado
CREATE INDEX IF NOT EXISTS idx_regions_state ON regions(state); 