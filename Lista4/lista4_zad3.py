"""
    Tworzenie interaktywnego wykresu modelu SEIR z wykorzystaniem biblioteki Dash.
"""

from dash import Dash, html, dcc, Output, Input
import plotly.express as px
from lista4 import seir_vals
from math import floor
import pandas as pd

app = Dash(__name__)


app.layout = html.Div([
    html.Div([html.H1('Model SEIR')], style={'textAlign': 'center'}),
    html.Label('N - liczba ludności'),
    dcc.Slider(min=200,
               max=1000,
               value=1000,
               step=50,
               tooltip={'placement': 'bottom', 'always_visible': True},
               updatemode='drag',
               persistence=True,
               persistence_type='session',
               id='N',
               ),
    html.Label('I - liczba zarażonych'),
    dcc.Slider(min=0,
               max=100,
               value=10,
               step=5,
               tooltip={'placement': 'bottom', 'always_visible': True},
               updatemode='drag',
               persistence=True,
               persistence_type='session',
               id='I',
               ),
    html.Div([
              html.Label('Beta (\u03B2) - wskaźnik infekcji'),
              dcc.Slider(min=0.1,
                         max=1.5,
                         value=0.4,
                         step=0.1,
                         tooltip={'placement': 'bottom', 'always_visible': True},
                         updatemode='drag',
                         persistence=True,
                         persistence_type='session',
                         id='beta',
                         )], style={'width': '33%', 'display': 'inline-block'}),
    html.Div([
             html.Label('Sigma (\u03C3) - wskaźnik inkubacji'),
             dcc.Slider(min=0.1,
                        max=1.5,
                        value=0.2,
                        step=0.1,
                        tooltip={'placement': 'bottom', 'always_visible': True},
                        updatemode='drag',
                        persistence=True,
                        persistence_type='session',
                        id='sigma',
                        )], style={'width': '33%', 'display': 'inline-block'}),
    html.Div([
              html.Label('Gamma (\u03B3) - wskaźnik wyzdrowień'),
              dcc.Slider(min=0.1,
                         max=1.5,
                         value=0.3,
                         step=0.1,
                         tooltip={'placement': 'bottom', 'always_visible': True},
                         updatemode='drag',
                         persistence=True,
                         persistence_type='session',
                         id='gamma',
                         )], style={'width': '33%', 'display': 'inline-block'}),
    html.Label('Czas symulacji (dni)'),
    dcc.Slider(min=50,
               max=200,
               value=100,
               step=10,
               tooltip={'placement': 'bottom', 'always_visible': True},
               updatemode='drag',
               persistence=True,
               persistence_type='session',
               id='t',
               ),
    dcc.Graph(id='seir_plot')
], style={'margin': 30})


@app.callback(
    Output('seir_plot', 'figure'),
    [Input('N', 'value'),
     Input('I', 'value'),
     Input('beta', 'value'), Input('sigma', 'value'), Input('gamma', 'value'), Input('t', 'value')]
)
def update_graph(N, I, beta, sigma, gamma, t):
    S = 2/3 * floor(N - I)
    E = N - I - S
    R = 0
    df = pd.DataFrame(seir_vals(N, S, E, I, R, beta, sigma, gamma, t),
                      columns=['Susceptible', 'Exposed', 'Infected', 'Recovered'])
    df['t'] = df.index
    fig = px.line(df, x='t', y=['Susceptible', 'Exposed', 'Infected', 'Recovered'], )
    fig.update_layout(title='Model SEIR', yaxis_title='Liczba ludności', xaxis_title='Czas (dni)',
                      legend_title='Zmienne', font=dict(size=15))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
