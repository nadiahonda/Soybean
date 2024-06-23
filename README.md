# Soybean Data Analysis

Este projeto é um aplicativo Streamlit para análise de dados de contratos contínuos de soja (ZS, ZL, ZM). Ele permite a atualização dos dados e a visualização de gráficos interativos.

## Estrutura do Projeto

- **data/**: Contém os arquivos parquet com os dados OHLCV.
- **scripts/**: Contém scripts para atualização e extração de dados.
- **app/**: Contém os componentes principais do aplicativo Streamlit.
- **requirements.txt**: Lista de dependências do projeto.
- **README.md**: Documentação do projeto.

## Como Executar

1. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

2. Execute o aplicativo Streamlit:
    ```bash
    streamlit run app/main.py
    ```

## Funcionalidades

- Atualização de dados OHLCV e relatórios COT.
- Visualização de gráficos interativos com Plotly.
- Filtro de intervalo de tempo através de um slider na barra lateral.
