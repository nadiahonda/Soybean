from lightweight_charts.widgets import StreamlitChart
import pandas as pd
import streamlit as st

def lightweight_chart_page(data, cot_data, symbol='ZS', interval='1D', markup=None):
    # st.title("OHLCV Lightweight Chart")

    # Utilização de lightweight-charts
    chart = StreamlitChart(width=1300, height=700, inner_width=1,
                           inner_height=0.7, toolbox=False)

    chart.legend(visible=True, font_size=12)
    chart.layout(background_color='#181c27', text_color='#b2b5be',
                 font_size=12, font_family='Century Gothic')
    chart.candle_style(up_color='#089981', down_color='#f23645', border_up_color='#089981', border_down_color='#f23645',
                       wick_up_color='#089981', wick_down_color='#f23645')
    chart.volume_config(up_color='#11443c', down_color='#5b2928')
    chart.price_line(line_visible=False)
    chart.fit()

    # Markups, se houver
    if markup is not None:
        for idx, row in data.iterrows():
            if row[markup] == 'up':
                chart.marker(time=row.name, position='below',
                             shape='arrow_up', color='#2196F3', text='up')
            elif row[markup] == 'down':
                chart.marker(time=row.name, position='above',
                             shape='arrow_down', color='#ffbf00', text='down')

    # Columns: | time | open | high | low | close | volume |
    chart.set(data)

    # Adicionar linha azul para o COT correspondente
    cot_column = f"{symbol}_COT_%"
    cot_series = cot_data[[cot_column]].reset_index()
    cot_series.columns = ['time', f'{symbol} COT %']

    chart2 = chart.create_subchart(
        position='bottom', width=0.992, height=0.3, sync=True)
    chart2.layout(background_color='#131722', text_color='#b2b5be',
                  font_size=12, font_family='Century Gothic')
    chart2.legend(visible=True, percent=True, lines=True, font_size=12)
    line = chart2.create_line(f'{symbol} COT %', price_label=True, price_line=False, color='#fb8c00')

    chart2.set()
    line.set(cot_series)

    # Adicionar linha horizontal em 0
    zero_line = pd.DataFrame({'time': cot_series['time'], 'zero': 0})
    zero_line_series = chart2.create_line('zero', color='#9598a1', width=1, style='solid', price_label=False, price_line=False)
    zero_line_series.set(zero_line)

    # Exibir o gráfico no Streamlit
    chart.load()

# Exemplo de uso
if __name__ == "__main__":
    # Carregar dados de exemplo
    zs_data = pd.read_parquet('path_to_zs_data.parquet')
    zl_data = pd.read_parquet('path_to_zl_data.parquet')
    zm_data = pd.read_parquet('path_to_zm_data.parquet')
    cot_data = pd.read_parquet('path_to_cot_data.parquet')

    # Selecionar o símbolo (exemplo)
    symbol = 'ZS'  # Pode ser 'ZS', 'ZL' ou 'ZM'
    data = zs_data if symbol == 'ZS' else zl_data if symbol == 'ZL' else zm_data

    lightweight_chart_page(data, cot_data, symbol=symbol)
