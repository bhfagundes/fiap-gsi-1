from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading
from crawler import AneelCrawler
from etl import EnergyETL
import pandas as pd
import time
import queue

class DataPipeline:
    def __init__(self):
        print("Inicializando pipeline...")
        self.crawler = AneelCrawler()
        self.etl = EnergyETL()
        self.data_queue = Queue(maxsize=20)
        self.batch_size = 10000
        self.total_processed = 0
        self.num_fetch_workers = 4  # Número de threads para busca
        
    def fetch_worker(self, worker_id, offset_start, offset_end):
        print(f"Worker {worker_id} iniciando coleta de {offset_start} até {offset_end}")
        try:
            while offset_start < offset_end:
                batch = self.crawler.fetch_batch(offset_start, self.batch_size)
                if batch:
                    df = pd.DataFrame(batch)
                    self.data_queue.put(df)
                    print(f"Worker {worker_id}: Coletados {len(batch)} registros")
                    offset_start += len(batch)
                else:
                    break
        except Exception as e:
            print(f"Erro no worker {worker_id}: {e}")
        finally:
            print(f"Worker {worker_id} finalizado")
            
    def process_worker(self):
        print("Iniciando processamento dos dados...")
        active_workers = self.num_fetch_workers
        consecutive_timeouts = 0
        max_timeouts = 3
        
        while active_workers > 0 or not self.data_queue.empty():
            try:
                df = self.data_queue.get(timeout=30)
                consecutive_timeouts = 0
                
                if df is not None and not df.empty:
                    print(f"Processando lote com {len(df)} registros...")
                    try:
                        df_transformed = self.etl.transform_consumption_data(df)
                        if df_transformed is not None and not df_transformed.empty:
                            self.etl.load_to_db(df_transformed, 'aneel_dados')
                            self.total_processed += len(df_transformed)
                            print(f"Lote processado com sucesso. Total: {self.total_processed} registros")
                        else:
                            print("Transformação resultou em DataFrame vazio")
                    except Exception as e:
                        print(f"Erro no processamento do lote: {str(e)[:200]}")
                
            except queue.Empty:
                if self.all_workers_finished:
                    break
                consecutive_timeouts += 1
                print(f"Timeout na fila ({consecutive_timeouts}/{max_timeouts})")
                if consecutive_timeouts >= max_timeouts:
                    print("Múltiplos timeouts consecutivos, reduzindo workers ativos")
                    active_workers -= 1
                    consecutive_timeouts = 0
            
    def run(self):
        print("Iniciando pipeline de dados...")
        start_time = time.time()
        
        self.all_workers_finished = False
        total_records = self.crawler.get_total_records()
        records_per_worker = total_records // self.num_fetch_workers
        
        with ThreadPoolExecutor(max_workers=self.num_fetch_workers + 1) as executor:
            futures = []
            for i in range(self.num_fetch_workers):
                offset_start = i * records_per_worker
                offset_end = offset_start + records_per_worker
                futures.append(
                    executor.submit(self.fetch_worker, i, offset_start, offset_end)
                )
            
            process_future = executor.submit(self.process_worker)
            
            for f in futures:
                f.result()
            
            self.all_workers_finished = True
            process_future.result()
        
        elapsed_time = time.time() - start_time
        print(f"\nPipeline concluído em {elapsed_time:.2f} segundos")
        print(f"Total processado: {self.total_processed} registros")

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run() 