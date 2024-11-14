from etl import EnergyETL

def process_all_metrics():
    print("Iniciando processamento das métricas...")
    etl = EnergyETL()
    
    try:
        print("\n1. Processando métricas diárias...")
        etl.process_daily_metrics()
        print("✓ Métricas diárias processadas")
        
        print("\n2. Calculando métricas per capita...")
        etl.calculate_per_capita_metrics()
        print("✓ Métricas per capita calculadas")
        
        print("\n3. Analisando tendências de consumo...")
        etl.analyze_consumption_trends()
        print("✓ Análise de tendências concluída")
        
        print("\nProcessamento de métricas concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")

if __name__ == "__main__":
    process_all_metrics() 