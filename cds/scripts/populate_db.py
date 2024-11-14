from crawler import AneelCrawler
from etl import EnergyETL
import pandas as pd

def main():
    crawler = AneelCrawler()
    etl = EnergyETL()
    
    raw_data = crawler.fetch_data()
    if raw_data:
        df = pd.DataFrame(raw_data)
        df_transformed = etl.transform_consumption_data(df)
        etl.load_to_db(df_transformed, 'consumption_data')
    
    etl.process_daily_metrics()

if __name__ == "__main__":
    main()