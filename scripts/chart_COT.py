import os
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

def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parquet_path = os.path.join(script_dir, '..', 'data', 'cot_soybean_products.parquet')
    df_COT = pd.read_parquet(parquet_path)
    return df_COT

def create_cot_figure(df_COT):
    max_ZS = df_COT['ZS_COT_%'].max()
    min_ZS = df_COT['ZS_COT_%'].min()
    max_ZL = df_COT['ZL_COT_%'].max()
    min_ZL = df_COT['ZL_COT_%'].min()
    max_ZM = df_COT['ZM_COT_%'].max()
    min_ZM = df_COT['ZM_COT_%'].min()

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    fig.add_trace(go.Scatter(
        x=df_COT.index, 
        y=df_COT['ZS_COT_%'], 
        mode='lines', 
        name='ZS_COT_%', 
        line=dict(color='#089981'), 
        hoverinfo='text',  # Use 'text' to control hover info
        hovertext=['{:.1f}%<br>{:%b %d, %y}'.format(y, x) for x, y in zip(df_COT.index, df_COT['ZS_COT_%'])]
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df_COT.index, 
        y=df_COT['ZL_COT_%'], 
        mode='lines', 
        name='ZL_COT_%', 
        line=dict(color='#fb8c00'), 
        hoverinfo='text',  # Use 'text' to control hover info
        hovertext=['{:.1f}%<br>{:%b %d, %y}'.format(y, x) for x, y in zip(df_COT.index, df_COT['ZL_COT_%'])]
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=df_COT.index, 
        y=df_COT['ZM_COT_%'], 
        mode='lines', 
        name='ZM_COT_%', 
        line=dict(color='#f23645'), 
        hoverinfo='text',  # Use 'text' to control hover info
        hovertext=['{:.1f}%<br>{:%b %d, %y}'.format(y, x) for x, y in zip(df_COT.index, df_COT['ZM_COT_%'])]
    ), row=3, col=1)

    fig.add_trace(go.Scatter(
        x=[df_COT.index[0], df_COT.index[-1]], 
        y=[max_ZS, max_ZS], 
        mode='lines', 
        line=dict(dash='dot', color='#9598a1'), 
        showlegend=False
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=[df_COT.index[0], df_COT.index[-1]], 
        y=[min_ZS, min_ZS], 
        mode='lines', 
        line=dict(dash='dot', color='#9598a1'), 
        showlegend=False
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=[df_COT.index[0], df_COT.index[-1]], 
        y=[max_ZL, max_ZL], 
        mode='lines', 
        line=dict(dash='dot', color='#9598a1'), 
        showlegend=False
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=[df_COT.index[0], df_COT.index[-1]], 
        y=[min_ZL, min_ZL], 
        mode='lines', 
        line=dict(dash='dot', color='#9598a1'), 
        showlegend=False
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=[df_COT.index[0], df_COT.index[-1]], 
        y=[max_ZM, max_ZM], 
        mode='lines', 
        line=dict(dash='dot', color='#9598a1'), 
        showlegend=False
    ), row=3, col=1)
    
    fig.add_trace(go.Scatter(
        x=[df_COT.index[0], df_COT.index[-1]], 
        y=[min_ZM, min_ZM], 
        mode='lines', 
        line=dict(dash='dot', color='#9598a1'), 
        showlegend=False
    ), row=3, col=1)

    fig.update_layout(
        height=800, 
        width=1200, 
        title_text="COT Soybean Products Over Time",
        template='custom_template',
        paper_bgcolor='#181c27',
        plot_bgcolor='#181c27',
        font=dict(color='#b2b5be')
    )

    fig.update_yaxes(title_text="ZS_COT_%", row=1, col=1, zerolinecolor='#9598a1', gridcolor='#2a2e39', dtick=10)
    fig.update_yaxes(title_text="ZL_COT_%", row=2, col=1, zerolinecolor='#9598a1', gridcolor='#2a2e39', dtick=10)
    fig.update_yaxes(title_text="ZM_COT_%", row=3, col=1, zerolinecolor='#9598a1', gridcolor='#2a2e39', dtick=10)
    fig.update_xaxes(zerolinecolor='#9598a1', gridcolor='#2a2e39')

    return fig

if __name__ == "__main__":
    df_COT = load_data()
    fig = create_cot_figure(df_COT)
    fig.show()
