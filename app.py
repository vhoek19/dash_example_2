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
    
    html.Div([
        
        html.Div([
            dcc.Dropdown(   # create drop down menu
                id = 'xaxis-column',
                options = [{'label': i, 'value': i} for i in available_indicators],  # do this for all available indicators
                value = 'Gross domestic product at market prices' # start value
            )
        ],
        style={'width': '24%', 'display': 'inline-block'}),  # this div will take half of the space

        html.Div([
            dcc.Dropdown(  # create a second drop down menu with 
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Compensation of employees'
            )
        ],
        style={'width': '24%', 'float': 'left', 'display': 'inline-block'}) #this takes the other size, if you take 100% the div will just be place down
    ]),

    dcc.Graph(id='indicator-graphic'),
        dcc.Slider(
        id='year--slider',
        min=df['Time'].min(),
        max=df['Time'].max(),
        value=df['Time'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Time'].unique()}             
    )
],style={'width': '48%', 'float': 'left', 'display': 'inline-block'})

@app.callback(   
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['Time'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator'] == yaxis_column_name]['Country'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name
            },
            yaxis={
                'title': yaxis_column_name
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

