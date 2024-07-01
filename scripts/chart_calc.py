import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Definir o template personalizado
custom_template = {
    'layout': {
        'template': 'plotly_white',
        'paper_bgcolor': '#181c27',
        'plot_bgcolor': '#181c27',
        'font': {'color': '#b2b5be'},
        'legend': {
            'orientation': "v",
            'yanchor': "top",
            'y': 1.10,
            'xanchor': "left",
            'x': 0.85  # Mover a legenda um pouco para a esquerda
        },
        'hovermode': 'x',
        'spikedistance': -1,
        'xaxis': {
            'showspikes': True,
            'spikecolor': "#b2b5be",
            'spikemode': "across",
            'spikesnap': "cursor",
            'showline': False,
            'gridcolor': '#2a2e39',
            'zerolinecolor': '#9598a1',
            'spikethickness': 1,
            'zerolinewidth': 0.5
        },
        'yaxis': {
            'showspikes': True,
            'spikecolor': "#b2b5be",
            'spikemode': "across",
            'spikesnap': "cursor",
            'showline': True,
            'gridcolor': '#2a2e39',
            'zerolinecolor': '#9598a1',
            'spikethickness': 1,
            'zerolinewidth': 0.5
        }
    }
}

# Registrar o template personalizado
pio.templates['custom_template'] = custom_template

def create_crush_spread_oil_share_figure(df_ZS, df_ZL, df_ZM):
    # Alinhar os índices dos DataFrames
    df_ZS, df_ZL = df_ZS.align(df_ZL, join='inner', axis=0)
    df_ZS, df_ZM = df_ZS.align(df_ZM, join='inner', axis=0)
    
    # Combine os dados em um único DataFrame, mantendo o índice de ZS1!
    data_combined = pd.DataFrame({
        'ZL1!': df_ZL['close'].values,
        'ZM1!': df_ZM['close'].values,
        'ZS1!': df_ZS['close'].values
    }, index=df_ZS.index)

    # Calcular a fórmula personalizada do Crush Spread
    data_combined['crush_spread'] = data_combined['ZL1!'] * 0.11 + data_combined['ZM1!'] * 0.022 - data_combined['ZS1!'] / 100
    # Calcular o Oil Share
    data_combined['oil_share'] = (data_combined['ZL1!'] * 0.11) / (data_combined['ZL1!'] * 0.11 + data_combined['ZM1!'] * 0.022)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    # Crush Spread Plot
    fig.add_trace(go.Scatter(
        x=data_combined.index, 
        y=data_combined['crush_spread'], 
        mode='lines', 
        name='Crush Spread', 
        line=dict(color='#089981'), 
        hoverinfo='text', 
        hovertext=['{:.2f}<br>{:%b %d, %y}'.format(y, x) for x, y in zip(data_combined.index, data_combined['crush_spread'])]
    ), row=1, col=1)
    
    # Adicionar linhas horizontais para o máximo e mínimo valor do Crush Spread
    max_crush_spread = data_combined['crush_spread'].max()
    min_crush_spread = data_combined['crush_spread'].min()
    fig.add_trace(go.Scatter(
        x=[data_combined.index[0], data_combined.index[-1]], 
        y=[max_crush_spread, max_crush_spread], 
        mode='lines', 
        line=dict(dash='dot', color='#9598a1'), 
        showlegend=False
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=[data_combined.index[0], data_combined.index[-1]], 
        y=[min_crush_spread, min_crush_spread], 
        mode='lines', 
        line=dict(dash='dot', color='#9598a1'), 
        showlegend=False
    ), row=1, col=1)

    # Oil Share Plot
    fig.add_trace(go.Scatter(
        x=data_combined.index, 
        y=data_combined['oil_share'], 
        mode='lines', 
        name='Oil Share', 
        line=dict(color='#fb8c00'), 
        hoverinfo='text', 
        hovertext=['{:.2f}<br>{:%b %d, %y}'.format(y, x) for x, y in zip(data_combined.index, data_combined['oil_share'])]
    ), row=2, col=1)

    # Adicionar linhas horizontais para o máximo e mínimo valor do Oil Share
    max_oil_share = data_combined['oil_share'].max()
    min_oil_share = data_combined['oil_share'].min()
    fig.add_trace(go.Scatter(
        x=[data_combined.index[0], data_combined.index[-1]], 
        y=[max_oil_share, max_oil_share], 
        mode='lines', 
        line=dict(dash='dot', color='#9598a1'), 
        showlegend=False
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=[data_combined.index[0], data_combined.index[-1]], 
        y=[min_oil_share, min_oil_share], 
        mode='lines', 
        line=dict(dash='dot', color='#9598a1'), 
        showlegend=False
    ), row=2, col=1)

    fig.update_layout(
        height=600, 
        width=1200, 
        title_text="Crush Spread and Oil Share Over Time",
        template='custom_template',
        paper_bgcolor='#181c27',
        plot_bgcolor='#181c27',
        font=dict(color='#b2b5be')
    )

    fig.update_yaxes(title_text="Crush Spread", row=1, col=1, zerolinecolor='#9598a1', gridcolor='#2a2e39')
    fig.update_yaxes(title_text="Oil Share", row=2, col=1, zerolinecolor='#9598a1', gridcolor='#2a2e39')
    fig.update_xaxes(zerolinecolor='#9598a1', gridcolor='#2a2e39')

    return fig

if __name__ == "__main__":
    # Exemplo de carregamento de dados para teste
    df_ZS = pd.read_parquet('data/ZS_1D.parquet')
    df_ZL = pd.read_parquet('data/ZL_1D.parquet')
    df_ZM = pd.read_parquet('data/ZM_1D.parquet')
    
    fig = create_crush_spread_oil_share_figure(df_ZS, df_ZL, df_ZM)
    fig.show()
