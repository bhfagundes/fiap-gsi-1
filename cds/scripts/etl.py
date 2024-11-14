import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import glob
from dotenv import load_dotenv
import os
import traceback

class EnergyETL:
    def __init__(self):
        load_dotenv()
        
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@" \
                 f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        
        self.engine = create_engine(db_url)
        self.setup_regions()
        
    def setup_regions(self):
        create_regions_table = """
        CREATE TABLE IF NOT EXISTS regions (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            state VARCHAR(2)
        );
        """
        
        regions_data = [
            ('Norte', None),
            ('Nordeste', None),
            ('Centro-Oeste', None),
            ('Sudeste', None),
            ('Sul', None)
        ]
        
        with self.engine.begin() as conn:
            conn.execute(text(create_regions_table))
            
            for region, state in regions_data:
                conn.execute(
                    text("INSERT INTO regions (name, state) VALUES (:name, :state) ON CONFLICT (name) DO NOTHING"),
                    {"name": region, "state": state}
                )
            
    def transform_consumption_data(self, df):
        try:
            if df.empty:
                print("DataFrame de entrada está vazio")
                return pd.DataFrame()
            
            print(f"Iniciando transformação de {len(df)} registros")
            df_cleaned = df.copy()
            
            # Remover sufixos numéricos e duplicatas
            df_cleaned.columns = df_cleaned.columns.str.replace(r'_m\d+$', '', regex=True)
            df_cleaned = df_cleaned.loc[:,~df_cleaned.columns.duplicated()]
            
            print(f"Colunas após limpeza: {', '.join(df_cleaned.columns)}")
            
            # Mapeamento das colunas
            column_mapping = {
                'DatGeracaoConjuntoDados': 'data_geracao',
                'AnmPeriodoReferencia': 'periodo_referencia',
                'SigUF': 'estado',
                'NomMunicipio': 'municipio',
                'SigTipoConsumidor': 'tipo_consumidor',
                'DscClasseConsumo': 'classe_consumo',
                'DscSubGrupoTarifario': 'grupo_tarifario',
                'MdaPotenciaInstaladaKW': 'potencia_instalada_kw',
                'QtdUCRecebeCredito': 'quantidade_uc',
                'NumCoordNEmpreendimento': 'latitude',
                'NumCoordEEmpreendimento': 'longitude',
                'DscModalidadeHabilitado': 'tensao_fornecimento',
                'DscPorte': 'grupo_tensao',
                'SigModalidadeEmpreendimento': 'situacao_ativacao',
                'DthAtualizaCadastralEmpreend': 'data_conexao',
                'DscFonteGeracao': 'fonte_energia'
            }
            
            # Renomear colunas existentes apenas
            existing_cols = {k: v for k, v in column_mapping.items() if k in df_cleaned.columns}
            df_cleaned = df_cleaned.rename(columns=existing_cols)
            
            # Garantir que todas as colunas necessárias existam
            required_columns = [
                'region_id', 'data_geracao', 'periodo_referencia', 'estado', 
                'municipio', 'tipo_consumidor', 'classe_consumo', 'grupo_tarifario',
                'potencia_instalada_kw', 'quantidade_uc', 'latitude', 'longitude',
                'tensao_fornecimento', 'grupo_tensao', 'situacao_ativacao',
                'data_conexao', 'fonte_energia'
            ]
            
            for col in required_columns:
                if col not in df_cleaned.columns:
                    df_cleaned[col] = None
            
            # Conversões de tipos
            df_cleaned['data_geracao'] = pd.to_datetime(df_cleaned['data_geracao'])
            df_cleaned['data_conexao'] = pd.to_datetime(df_cleaned['data_conexao'])
            
            # Tratamento de valores numéricos
            numeric_cols = ['latitude', 'longitude', 'potencia_instalada_kw', 'quantidade_uc']
            for col in numeric_cols:
                if col in df_cleaned.columns:
                    df_cleaned[col] = df_cleaned[col].replace('', None)
                    mask = df_cleaned[col].notna()
                    df_cleaned.loc[mask, col] = df_cleaned.loc[mask, col].astype(str).str.replace(',', '.').astype(float)
            
            # Adicionar region_id
            estado_regiao = {
                'AC': 1, 'AM': 1, 'AP': 1, 'PA': 1, 'RO': 1, 'RR': 1, 'TO': 1,
                'AL': 2, 'BA': 2, 'CE': 2, 'MA': 2, 'PB': 2, 'PE': 2, 'PI': 2, 'RN': 2, 'SE': 2,
                'DF': 3, 'GO': 3, 'MT': 3, 'MS': 3,
                'ES': 4, 'MG': 4, 'RJ': 4, 'SP': 4,
                'PR': 5, 'RS': 5, 'SC': 5
            }
            df_cleaned['region_id'] = df_cleaned['estado'].map(estado_regiao)
            
            # Limitar tamanho dos campos de texto
            text_limits = {
                'tipo_consumidor': 50,
                'classe_consumo': 50,
                'tensao_fornecimento': 50,
                'grupo_tensao': 50,
                'situacao_ativacao': 50,
                'fonte_energia': 100,
                'grupo_tarifario': 50,
                'municipio': 100,
                'estado': 2
            }
            
            for col, limit in text_limits.items():
                if col in df_cleaned.columns:
                    df_cleaned[col] = df_cleaned[col].astype(str).str[:limit]
            
            print(f"Transformação concluída. Registros resultantes: {len(df_cleaned)}")
            return df_cleaned[required_columns]
            
        except Exception as e:
            print(f"Erro na transformação dos dados: {str(e)[:200]}")
            print(f"Colunas disponíveis: {', '.join(df.columns)}")
            return pd.DataFrame()
    
    def load_to_db(self, df, table_name='aneel_dados', batch_size=10000):
        if df.empty:
            print(f"DataFrame vazio, pulando inserção em {table_name}")
            return
        
        try:
            total_rows = len(df)
            print(f"Iniciando inserção de {total_rows} registros em {table_name}")
            
            # Garantir tipos de dados corretos antes da inserção
            df['data_geracao'] = pd.to_datetime(df['data_geracao'])
            df['data_conexao'] = pd.to_datetime(df['data_conexao'])
            df['potencia_instalada_kw'] = pd.to_numeric(df['potencia_instalada_kw'], errors='coerce')
            df['quantidade_uc'] = pd.to_numeric(df['quantidade_uc'], errors='coerce')
            df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
            df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
            
            # Divide o DataFrame em chunks para inserção em batch
            for i in range(0, total_rows, batch_size):
                chunk = df.iloc[i:i + batch_size]
                try:
                    chunk.to_sql(
                        table_name, 
                        self.engine, 
                        if_exists='append', 
                        index=False,
                        method='multi',
                        chunksize=batch_size
                    )
                    print(f"Inseridos {min(i + batch_size, total_rows)}/{total_rows} registros")
                except Exception as e:
                    print(f"Erro ao inserir chunk {i//batch_size + 1}: {str(e)[:200]}")
                    continue
                
        except Exception as e:
            print(f"Erro na inserção dos dados: {str(e)[:200]}")
    
    def process_daily_metrics(self):
        metrics_data = []
        raw_files = glob.glob('data/raw/aneel_*.csv')
        
        for file in raw_files:
            df = pd.read_csv(file)
            
            # Converter valores numéricos (tratando vírgula)
            df['MdaPotenciaInstaladaKW'] = df['MdaPotenciaInstaladaKW'].str.replace(',', '.').astype(float)
            
            df['data_registro'] = pd.to_datetime(df['DatGeracaoConjuntoDados'])
            
            # Agrupar por data
            daily_metrics = df.groupby(df['data_registro'].dt.date).agg({
                'MdaPotenciaInstaladaKW': ['mean', 'max']
            }).reset_index()
            
            # Renomear colunas
            daily_metrics.columns = ['data_registro', 'consumo_medio', 'pico_consumo']
            daily_metrics['economia_estimada'] = daily_metrics['consumo_medio'] * 0.2
            
            metrics_data.append(daily_metrics)
        
        if metrics_data:
            final_metrics = pd.concat(metrics_data)
            final_metrics.to_sql('metricas_diarias', self.engine, if_exists='append', index=False)
    
    def calculate_per_capita_metrics(self):
        query = """
        WITH consumo_agregado AS (
            SELECT 
                region_id,
                DATE_TRUNC('month', data_geracao) as periodo,
                SUM(potencia_instalada_kw) as demanda_total,
                COUNT(DISTINCT municipio) as num_municipios
            FROM aneel_dados
            GROUP BY region_id, DATE_TRUNC('month', data_geracao)
        )
        INSERT INTO consumo_regional (regiao_id, ano, mes, demanda_mw, consumo_per_capita)
        SELECT 
            region_id,
            EXTRACT(YEAR FROM periodo),
            EXTRACT(MONTH FROM periodo),
            demanda_total / 1000 as demanda_mw,
            (demanda_total / populacao) as consumo_per_capita
        FROM consumo_agregado
        JOIN regions r ON r.id = region_id;
        """
        with self.engine.begin() as conn:
            conn.execute(text(query))
    
    def analyze_consumption_trends(self):
        query = """
        WITH trends AS (
            SELECT 
                regiao_id,
                periodo,
                consumo_per_capita,
                LAG(consumo_per_capita) OVER (PARTITION BY regiao_id ORDER BY periodo) as consumo_anterior,
                100 * (consumo_per_capita - LAG(consumo_per_capita) OVER (
                    PARTITION BY regiao_id ORDER BY periodo
                )) / LAG(consumo_per_capita) OVER (
                    PARTITION BY regiao_id ORDER BY periodo
                ) as variacao
            FROM consumo_regional
        )
        INSERT INTO analise_tendencias (
            periodo, regiao_id, consumo_per_capita, 
            variacao_percentual, tendencia_consumo
        )
        SELECT 
            periodo,
            regiao_id,
            consumo_per_capita,
            variacao,
            CASE 
                WHEN variacao > 5 THEN 'AUMENTO'
                WHEN variacao < -5 THEN 'DIMINUIÇÃO'
                ELSE 'ESTÁVEL'
            END as tendencia
        FROM trends
        WHERE variacao IS NOT NULL;
        """
        with self.engine.begin() as conn:
            conn.execute(text(query))