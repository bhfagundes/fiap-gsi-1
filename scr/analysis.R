# Configurar mirror CRAN de forma robusta
set_cran_mirror <- function() {
    # Definir mirror padrão
    options(repos = structure(c(CRAN = "https://cloud.r-project.org")))
}

# Lista de pacotes necessários (baseado em ```457:460:aicss/readme.md```)
required_packages <- c(
    "stringi", "tidyverse", "plotly", "lubridate", 
    "scales", "gridExtra", "forecast", "ggplot2",
    "dplyr", "tidyr"
)

# Função para instalar pacotes
install_if_missing <- function(packages) {
    # Configurar mirror CRAN
    set_cran_mirror()
    
    new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
    if(length(new_packages)) {
        print(paste("Instalando pacotes:", paste(new_packages, collapse=", ")))
        for(pkg in new_packages) {
            tryCatch({
                install.packages(pkg, dependencies=TRUE)
                print(paste("✓ Pacote", pkg, "instalado com sucesso"))
            }, error = function(e) {
                print(paste("✗ Erro ao instalar", pkg, ":", e$message))
            })
        }
    }
}

# Instalar e carregar pacotes
install_if_missing(required_packages)
lapply(required_packages, library, character.only = TRUE)

# Configuração inicial
options(timeout = 600) # Aumenta timeout para 10 minutos

# Função para download em chunks
download_large_file <- function(url, dest_file) {
    print("Iniciando download do arquivo...")
    
    tryCatch({
        # Criar diretório se não existir
        dir.create(dirname(dest_file), recursive = TRUE, showWarnings = FALSE)
        
        # Download com progress bar
        download.file(
            url = url,
            destfile = dest_file,
            method = "auto",
            mode = "wb",
            quiet = FALSE
        )
        
        print("Download concluído!")
        return(TRUE)
    }, error = function(e) {
        print(paste("Erro no download:", e$message))
        return(FALSE)
    })
}

# Função para carregar dados em chunks
read_csv_chunks <- function(file, chunk_size = 100000) {
    print("Carregando dados em chunks...")
    
    con <- file(file, "r")
    header <- readLines(con, n = 1)
    chunks <- list()
    total_rows <- 0
    
    while (TRUE) {
        chunk <- read.csv(
            text = readLines(con, n = chunk_size),
            header = FALSE,
            col.names = strsplit(header, ",")[[1]]
        )
        
        if (nrow(chunk) == 0) break
        
        total_rows <- total_rows + nrow(chunk)
        chunks[[length(chunks) + 1]] <- chunk
        
        print(sprintf("Processados %d registros...", total_rows))
    }
    
    close(con)
    return(do.call(rbind, chunks))
}

# Função para análise dos dados
analyze_energy_data <- function(df) {
    print("Iniciando análise dos dados...")
    
    # Criar diretório para resultados
    dir.create("resultados", showWarnings = FALSE)
    dir.create("resultados/plots", showWarnings = FALSE)
    
    # Análises estatísticas
    summary_stats <- df %>%
        group_by(fonte_energia) %>%
        summarise(
            total_potencia = sum(potencia_instalada_kw, na.rm = TRUE),
            media_potencia = mean(potencia_instalada_kw, na.rm = TRUE),
            total_unidades = sum(quantidade_uc, na.rm = TRUE),
            n_instalacoes = n(),
            .groups = "drop"
        )
    
    # Análise temporal
    temporal_analysis <- df %>%
        mutate(ano = year(data_conexao)) %>%
        group_by(ano, fonte_energia) %>%
        summarise(
            potencia_total = sum(potencia_instalada_kw, na.rm = TRUE),
            .groups = "drop"
        )
    
    # Análise geográfica
    geographic_analysis <- df %>%
        group_by(estado) %>%
        summarise(
            potencia_total = sum(potencia_instalada_kw, na.rm = TRUE),
            .groups = "drop"
        )
    
    # Salvar resultados em CSV
    write.csv(summary_stats, "resultados/resumo_estatistico.csv", row.names = FALSE)
    write.csv(temporal_analysis, "resultados/analise_temporal.csv", row.names = FALSE)
    write.csv(geographic_analysis, "resultados/analise_geografica.csv", row.names = FALSE)
    
    # Gerar visualizações
    plots <- list()
    
    # 1. Distribuição por fonte
    png("resultados/plots/distribuicao_fontes.png", width = 800, height = 600)
    pie(summary_stats$total_potencia, 
        labels = summary_stats$fonte_energia,
        main = "Distribuição da Potência por Fonte")
    dev.off()
    
    # 2. Evolução temporal
    png("resultados/plots/evolucao_temporal.png", width = 800, height = 600)
    plot(temporal_analysis$ano, temporal_analysis$potencia_total,
         type = "l", col = "blue",
         main = "Evolução da Potência Instalada",
         xlab = "Ano", ylab = "Potência Total (kW)")
    dev.off()
    
    # 3. Distribuição geográfica
    png("resultados/plots/distribuicao_geografica.png", width = 800, height = 600)
    barplot(geographic_analysis$potencia_total,
            names.arg = geographic_analysis$estado,
            las = 2,
            main = "Potência Instalada por Estado",
            ylab = "Potência Total (kW)")
    dev.off()
    
    # Gerar relatório em TXT
    sink("resultados/relatorio_completo.txt")
    cat("RELATÓRIO DE ANÁLISE DE DADOS ENERGÉTICOS\n")
    cat("========================================\n\n")
    cat("1. RESUMO ESTATÍSTICO\n")
    print(summary_stats)
    cat("\n2. ANÁLISE TEMPORAL\n")
    print(head(temporal_analysis))
    cat("\n3. ANÁLISE GEOGRÁFICA\n")
    print(head(geographic_analysis))
    sink()
    
    print("✓ Análise concluída! Resultados salvos em /resultados")
    
    return(list(
        summary = summary_stats,
        temporal = temporal_analysis,
        geographic = geographic_analysis
    ))
}

# Função para verificar e baixar dados
get_aneel_data <- function(url, local_file) {
    if (file.exists(local_file)) {
        print("Arquivo já existe localmente. Pulando download...")
        return(TRUE)
    }
    
    print("Arquivo não encontrado localmente. Iniciando download...")
    tryCatch({
        # Criar diretório se não existir
        dir.create(dirname(local_file), recursive = TRUE, showWarnings = FALSE)
        
        # Download com progress bar
        download.file(
            url = url,
            destfile = local_file,
            method = "auto",
            mode = "wb",
            quiet = FALSE
        )
        
        print("Download concluído!")
        return(TRUE)
    }, error = function(e) {
        print(paste("Erro no download:", e$message))
        return(FALSE)
    })
}

# Função principal
main <- function() {
    # URL e arquivo local
    ANEEL_URL <- "https://dadosabertos.aneel.gov.br/dataset/5e0fafd2-21b9-4d5b-b622-40438d40aba2/resource/b1bd71e7-d0ad-4214-9053-cbd58e9564a7/download/empreendimento-geracao-distribuida.csv"
    local_file <- "data/raw/aneel_data.csv"
    
    # Verificar e baixar dados se necessário
    if (!get_aneel_data(ANEEL_URL, local_file)) {
        stop("Falha ao obter dados da ANEEL")
    }
    
    # Carregar e processar dados
    df <- read.csv(local_file, sep = ";", encoding = "UTF-8")
    
    # Verificar colunas disponíveis
    print("Colunas disponíveis:")
    print(colnames(df))
    
    # Preparar dados usando mapeamento correto
    df <- df %>%
        select_if(~!all(is.na(.))) %>%  # Remove colunas vazias
        rename_with(~gsub("_m\\d+$", "", .), everything()) %>%  # Remove sufixos numéricos
        rename(
            data_geracao = "DatGeracaoConjuntoDados",
            periodo_referencia = "AnmPeriodoReferencia",
            estado = "SigUF",
            municipio = "NomMunicipio",
            tipo_consumidor = "SigTipoConsumidor",
            classe_consumo = "DscClasseConsumo",
            grupo_tarifario = "DscSubGrupoTarifario",
            potencia_instalada_kw = "MdaPotenciaInstaladaKW",
            quantidade_uc = "QtdUCRecebeCredito",
            latitude = "NumCoordNEmpreendimento",
            longitude = "NumCoordEEmpreendimento",
            tensao_fornecimento = "DscModalidadeHabilitado",
            grupo_tensao = "DscPorte",
            situacao_ativacao = "SigModalidadeEmpreendimento",
            data_conexao = "DthAtualizaCadastralEmpreend",
            fonte_energia = "DscFonteGeracao"
        ) %>%
        mutate(
            data_conexao = as.Date(data_conexao),
            potencia_instalada_kw = as.numeric(gsub(",", ".", potencia_instalada_kw)),
            latitude = as.numeric(gsub(",", ".", latitude)),
            longitude = as.numeric(gsub(",", ".", longitude))
        )

    # Realizar análise
    results <- analyze_energy_data(df)
    
    # Gerar relatório
    rmarkdown::render(
        "report.Rmd",
        output_file = "relatorio_energia.html",
        params = list(
            results = results,
            data = df
        )
    )
    
    print("Análise concluída! Relatório gerado em 'relatorio_energia.html'")
}

# Executar análise
if (!interactive()) {
    main()
} 