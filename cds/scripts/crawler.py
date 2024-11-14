import requests
import pandas as pd
from datetime import datetime
import os
import json
import time

class AneelCrawler:
    def __init__(self):
        self.base_url = "https://dadosabertos.aneel.gov.br/api/3/action/datastore_search"
        self.resource_id = "b1bd71e7-d0ad-4214-9053-cbd58e9564a7"
        
    def fetch_data(self):
        all_records = []
        offset = 0
        limit = 100000
        total_records = None
        
        while True:
            params = {
                "resource_id": self.resource_id,
                "limit": limit,
                "offset": offset,
                "sort": "DatGeracaoConjuntoDados asc"
            }
            
            try:
                response = requests.get(self.base_url, params=params)
                print(f"URL da requisição: {response.url}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        result = data.get("result", {})
                        
                        if total_records is None:
                            total_records = result.get("total", 0)
                            print(f"Total de registros disponíveis: {total_records}")
                        
                        records = result.get("records", [])
                        if not records:
                            print("Nenhum registro encontrado neste lote")
                            break
                        
                        all_records.extend(records)
                        offset += len(records)
                        
                        progress = min(100, (len(all_records) / total_records) * 100)
                        print(f"Progresso: {progress:.1f}% | Registros coletados: {len(all_records)}/{total_records}")
                        
                        if len(all_records) >= total_records:
                            break
                            
                        time.sleep(1)
                    else:
                        print(f"Erro nos dados: {data}")
                        break
                else:
                    print(f"Status code: {response.status_code}")
                    print(f"Resposta: {response.text}")
                    break
                    
            except requests.exceptions.RequestException as e:
                print(f"Erro na requisição: {e}")
                print("Tentando novamente em 5 segundos...")
                time.sleep(5)
                continue
        
        print(f"Total final de registros: {len(all_records)}")
        return all_records

    def save_raw_data(self, data, year):
        if not data:
            return
            
        if not os.path.exists('data/raw'):
            os.makedirs('data/raw')
        
        df = pd.DataFrame(data)
        output_path = f'data/raw/aneel_{year}.csv'
        df.to_csv(output_path, index=False)
        print(f"Dados salvos em {output_path}")

    def fetch_batch(self, offset, limit):
        params = {
            "resource_id": self.resource_id,
            "limit": limit,
            "offset": offset,
            "sort": "DatGeracaoConjuntoDados asc"
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    records = data.get("result", {}).get("records", [])
                    return records
        except Exception as e:
            print(f"Erro ao buscar lote: {e}")
        return None

    def get_total_records(self):
        """Obtém o número total de registros disponíveis na API"""
        params = {
            "resource_id": self.resource_id,
            "limit": 1
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    result = data.get("result", {})
                    total = result.get("total", 0)
                    print(f"Total de registros disponíveis: {total}")
                    return total
        except Exception as e:
            print(f"Erro ao obter total de registros: {e}")
        
        return 0