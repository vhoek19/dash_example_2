
# coding: utf-8

# In[44]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)   # changed this to deployment 
server= app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv('nama_10_gdp_1_Data.csv')
df = df.rename(columns={'NA_ITEM': 'Indicator', 'TIME': 'Time', 'GEO': 'Country', 'UNIT': 'Unit'})
searchfor = ['Euro']
df = df[~df.Country.str.contains('|'.join(searchfor))]
df

available_indicators = df['Indicator'].unique()
available_countries = df['Country'].unique()

app.layout = html.Div([
    html.H1('Dashboard Eurostat: GDP and main components (output, expenditure and income)',
                style={'textAlign': 'center', 'font-family':'arial,calibri,serif'}),
# Graph 1 - block
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column-a',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'  # start value
            ),
            dcc.RadioItems(
                id='xaxis-type-a',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),  # this div will take half of the space

        html.Div([
            dcc.Dropdown(
                id='yaxis-column-a',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Compensation of employees'
            ),
            dcc.RadioItems(
                id='yaxis-type-a',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'display': 'inline-block'}) #this takes the other size, if you take 100% the div will just be place down
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['Time'].min(),
        max=df['Time'].max(),
        value=df['Time'].max(),
        step=None,
        marks={str(year): {'label' : str(year), 'style':{'color':'rgb(74, 76, 79)'}}
               for year in df['Time'].unique()}
    ),
        html.Div([], style={'height': '50px'}),
    
# Graph 2 - block
   
        html.Div([
          html.Div([
            dcc.Dropdown(
                id='xaxis-column-b',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Belgium'  # start value
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),  # this div will take half of the space
    
        html.Div([
            dcc.Dropdown(
                id='yaxis-column-b',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices',
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}) #this takes the other size, if you take 100% the div will just be place down
    ]),
    
    html.Div([], style={'height': '50px'}),

    dcc.Graph(id='indicator-graphic2'),
])

# Graph 1 - block

@app.callback(   
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column-a', 'value'),
     dash.dependencies.Input('yaxis-column-a', 'value'),
     dash.dependencies.Input('xaxis-type-a', 'value'),
     dash.dependencies.Input('yaxis-type-a', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    
    dff = df[df['Time'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator'] == yaxis_column_name]['Country'],
            mode='markers',
            marker = dict(
                size = 10,
                color = 'rgba(255, 182, 193, .9)',
                line = dict(
                    width = 4)),
            line = dict(
                color = 'rgb(205, 12, 24)',
                width = 4)
        )],
        'layout': go.Layout(
            title = "<br><b>Indicator Correlation",
            xaxis=dict(
                title = xaxis_column_name,
                type = 'linear' if xaxis_type == 'Linear' else 'log',
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(74, 76, 79)',
                linewidth=2,
                ticks='outside',
                tickcolor='rgb(74, 76, 79)',
                tickwidth=2,
                ticklen=5,
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                title = yaxis_column_name,
                type = 'linear' if yaxis_type == 'Linear' else 'log',
                showline=True,
                showgrid = True,
                showticklabels=True,
                linecolor='rgb(74, 76, 79)',
                linewidth=2,
                ticks='outside',
                tickcolor='rgb(74, 76, 79)',
                tickwidth=2,
                ticklen=5,
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            margin={'l': 90, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

# Graph 2 - block

@app.callback(   
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('xaxis-column-b', 'value'),
     dash.dependencies.Input('yaxis-column-b', 'value')])

def update_graph2(xaxis_column_name_b, yaxis_column_name_b):
    
    dff1 = df[df['Unit'] == "Current prices, million euro"]
    dff2 = dff1[dff1['Country'] == xaxis_column_name_b]
    
    return {
        'data': [go.Scatter(
            x=dff2['Time'].unique(),
            y=dff2[dff2['Indicator'] == yaxis_column_name_b]['Value'],
            text=dff2[dff2['Indicator'] == yaxis_column_name_b]['Time'],
            mode='lines+markers',
            marker = dict(
                size = 10,
                color = 'rgba(255, 182, 193, .9)',
                line = dict(
                    width = 4)),
            line = dict(
                color = 'rgb(205, 12, 24)',
                width = 4)
        )],
        'layout': go.Layout(
            title = "<br><b>Indicator Development from 2008 to 2017",
            xaxis=dict(
                title = xaxis_column_name_b,
                type = 'log',
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(74, 76, 79)',
                linewidth=2,
                ticks='outside',
                tickcolor='rgb(74, 76, 79)',
                tickwidth=2,
                ticklen=5,
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                title = yaxis_column_name_b,
                showline=True,
                showgrid = True,
                showticklabels=True,
                linecolor='rgb(74, 76, 79)',
                linewidth=2,
                ticks='outside',
                tickcolor='rgb(74, 76, 79)',
                automargin=True,
                tickwidth=2,
                ticklen=5,
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            margin={'l': 90, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True))

