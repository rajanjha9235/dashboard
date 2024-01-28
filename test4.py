import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year


app.layout = html.Div(children=[
    html.H1('Australia Wildfire Dashboard', style={'font-size':26,'text-align':'center'}),
    html.Div([
        html.Div([
            html.H2('Select Region : ',style={'margin-right':'2em'}),
            dcc.RadioItems([
                {'label':'New South Vales','value':'NSW'},
                {'label': 'Northern Teritorry', 'value': 'NT'},
                {'label':'Queensland', 'value':'QL'},
                {'label':'South Australia', 'value':'SA'},
                {'label':'Tasmania', 'value':'TA'},
                {'label':'Victoria', 'value':'VI'},
                {'label':'Western Australia', 'value':'WA'}
            ], 'NSW', id='region', inline=True)
        ]),
        html.Div([
            html.H2('Select Year', style={'margin-right':'2em'}),
            dcc.Dropdown(df.Year.unique(),value=2005, id='year')
        ]),
        html.Div([
            html.Div([],id = 'plot1'),
            html.Div([],id = 'plot2')
        ], style= {'display':'flex'})
    ])
])

@app.callback([Output(component_id='plot1',component_property='children'),
               Output(component_id='plot2', component_property='children')],
               [Input(component_id='region', component_property='value'),
                Input(component_id='year', component_property='value')])

def get_graph(input_region, input_year):
    region_data = df[df['Region']==input_region]
    year_data = region_data[region_data['Year']== input_year]

    est_data = year_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data,values='Estimated_fire_area', names='Month', title=f'{input_region} : Monthly Average Estimated Area in year {input_year}.')

    veg_data = year_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data, x='Month', y='Count', title=f'{input_region} Average Count of pixels for presumed Vegetarian Fires in year {input_year}.')

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]

if __name__ == '__main__':
    app.run()