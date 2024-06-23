import streamlit as st
import pandas as pd
import plotly.io as pio
from scripts.update_data import update_ohlcv_data, update_cot_reports
from scripts.chart_COT import create_cot_figure, load_data
from scripts.chart_calc import create_crush_spread_oil_share_figure

# Forçar o Plotly a usar o motor de serialização padrão do Python
pio.orca.config.use_xvfb = True

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Adicionar estilo CSS para definir o fundo da página, do cabeçalho e reduzir espaços no topo
st.markdown(
    """
    <style>
    .main {
        background-color: #181c27;
        color: #b2b5be;
    }
    .sidebar .sidebar-content {
        background-color: #181c27;
        color: #b2b5be;
    }
    /* Estilo para o cabeçalho */
    .css-18ni7ap.e8zbici2 {
        background-color: #181c27;
        color: #b2b5be;
    }
    .css-1v3fvcr.e8zbici0 {
        color: #b2b5be;
    }
    /* Ajustar a largura dos dropdowns */
    .stSelectbox > div > div {
        width: 100% !important;
    }
    /* Centralizar as legendas com os dropdowns */
    .legend-header {
        text-align: center;
        width: 100%;
        display: inline-block;
    }
    /* Ajustar a largura das colunas */
    .stColumn > div {
        display: flex;
        justify-content: center;
    }
    /* Estilo para o botão de atualização */
    .full-width-button > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def load_ohlcv_data():
    # Function to load data from parquet files
    zs_data = pd.read_parquet('data/ZS_1D.parquet')
    zl_data = pd.read_parquet('data/ZL_1D.parquet')
    zm_data = pd.read_parquet('data/ZM_1D.parquet')
    return zs_data, zl_data, zm_data

def checklist():
    st.sidebar.write('<style>div[data-testid="column"]:nth-child(2) div, div[data-testid="column"]:nth-child(3) div, div[data-testid="column"]:nth-child(4) div {text-align: center;}</style>', unsafe_allow_html=True)
    
    # Definir os símbolos
    symbols = ["🟢", "🔴", "🟡"]

    # Definir as linhas e colunas
    rows = ["COT", "Crush Spread", "Oil Share", "Price Action"]
    columns = ["ZS", "ZL", "ZM"]

    # Criar um DataFrame inicial com todos os valores amarelos
    data = {col: ["🟡"] * len(rows) for col in columns}
    df = pd.DataFrame(data, index=rows)

    # Renderizar a tabela com dropdowns na barra lateral
    header_cols = st.sidebar.columns([0.7, 1, 1, 1])
    header_cols[1].markdown("<div class='legend-header'>ZS</div>", unsafe_allow_html=True)
    header_cols[2].markdown("<div class='legend-header'>ZL</div>", unsafe_allow_html=True)
    header_cols[3].markdown("<div class='legend-header'>ZM</div>", unsafe_allow_html=True)
    
    for row in rows:
        cols = st.sidebar.columns([0.7, 1, 1, 1])  # Ajustar o tamanho das colunas
        cols[0].write(f"**{row}**")
        for i, col in enumerate(columns):
            df.at[row, col] = cols[i + 1].selectbox(f"Select symbol for {row} {col}", symbols, index=2, key=f"{row}_{col}", label_visibility='collapsed')

    return df

def main():
    
    # Sidebar
    st.sidebar.header("Inputs")
    year_range = st.sidebar.slider("Select Year Range", min_value=2013, max_value=2024, value=(2018, 2024))
    start_year, end_year = year_range
    
    # Adicionar espaço antes do botão
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    
    # Exibir a tabela de inputs na barra lateral
    df = checklist()
    
    # Adicionar espaço antes do botão
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    
    # Espaço reservado para o botão de atualização
    update_button_placeholder = st.sidebar.empty()
    
    # Button to update data in the sidebar
    with update_button_placeholder.container():
        if st.sidebar.button("Update Data", key="update_button", help="Clique para atualizar os dados"):
            update_ohlcv_data()
            update_cot_reports()
            st.sidebar.success("Data updated successfully!")
            # Recarregar os dados após a atualização
            zs_data, zl_data, zm_data = load_ohlcv_data()
            cot_data = load_data()
        else:
            # Carregar os dados inicialmente
            zs_data, zl_data, zm_data = load_ohlcv_data()
            cot_data = load_data()
    
    # Convert index to datetime if not already
    zs_data.index = pd.to_datetime(zs_data.index)
    zl_data.index = pd.to_datetime(zl_data.index)
    zm_data.index = pd.to_datetime(zm_data.index)
    cot_data.index = pd.to_datetime(cot_data.index)
    
    # Filter data by date range
    zs_filtered = zs_data[(zs_data.index.year >= start_year) & (zs_data.index.year <= end_year)]
    zl_filtered = zl_data[(zl_data.index.year >= start_year) & (zl_data.index.year <= end_year)]
    zm_filtered = zm_data[(zm_data.index.year >= start_year) & (zm_data.index.year <= end_year)]
    cot_filtered = cot_data[(cot_data.index.year >= start_year) & (cot_data.index.year <= end_year)]
    
    # Dividir a tela em duas colunas
    col1, col2 = st.columns(2)
    
    with col1:
        # Display COT chart
        st.plotly_chart(create_cot_figure(cot_filtered), use_container_width=True)
    
    with col2:
        # Display Crush Spread and Oil Share chart
        st.plotly_chart(create_crush_spread_oil_share_figure(zs_filtered, zl_filtered, zm_filtered), use_container_width=True)
        
        # Adicionar espaço vertical reduzido entre o gráfico e a checklist
        st.markdown("<div style='margin-top: -20px;'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
