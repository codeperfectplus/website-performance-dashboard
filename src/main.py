from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import datetime
import io
import os
import plotly.graph_objects as go
import base64
import traceback

app = Dash(__name__)

ROOT_DIR = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# if there is zip file in the data directory unzip it and replace the existing file
for file in os.listdir(DATA_DIR):
    if file.endswith('.zip'):
        os.system(f'unzip -o {os.path.join(DATA_DIR, file)} -d {DATA_DIR}')

def load_csv_files(filepath):
    if filepath.endswith('.csv') and os.path.exists(filepath):
        return pd.read_csv(filepath)
    return pd.DataFrame()

countries_df = load_csv_files(os.path.join(DATA_DIR, 'Countries.csv'))
dates_df = load_csv_files(os.path.join(DATA_DIR, 'Dates.csv'))
devices_df = load_csv_files(os.path.join(DATA_DIR, 'Devices.csv'))
filter_df = load_csv_files(os.path.join(DATA_DIR, 'Filters.csv'))
pages_df = load_csv_files(os.path.join(DATA_DIR, 'Pages.csv'))
queries_df = load_csv_files(os.path.join(DATA_DIR, 'Queries.csv'))    


dates_df['Date'] = pd.to_datetime(dates_df['Date'])
dates_df['Day'] = dates_df['Date'].dt.day_name()


app.layout = html.Div([
    html.H1('Google Analytics Dashboard by CodePerfectPlus', 
            style={'text-align': 'center', 'color': 'black', 'margin-top': '2%', 'margin-bottom': '2%'}),
    
    html.H2('Upload your data to see the dashboard', style={'text-align': 'center'}),
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin-bottom': '2%'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
    ]),
    dcc.Interval(
        id="load_interval", 
        n_intervals=0, 
        max_intervals=0, #<-- only run once
        interval=1
    ),
    # create a line here
    html.Hr(),
    
    html.Div([
        # datepicker 
        html.Div([
            html.Div([
                dcc.DatePickerRange(
                    id='date-picker',
                    start_date=datetime.date(2024, 1, 1),
                    end_date=datetime.date(2024, 12, 31),
                    display_format='YYYY-MM-DD',
                    style={'margin-right': '10px', 'height': '60px', 'width': '40%'}
                ),
                dash_table.DataTable(id='total_clicks_impressions', 
                                     style_cell={'textAlign': 'center'}, 
                                     style_header={'backgroundColor': 'lightblue'}, 
                                     style_data={'backgroundColor': 'white'}),
                # create both item side by side little space between them in center of the site beautifully
            ], style={'display': 'flex', 'justify-content': 'center' })
        ]),
        # styble table in centre of the page and style with bootstrap color and width and margin from left and right 10%
        
        dcc.Graph(id='overall-traffic'),
        dcc.Graph(id='day-wise-click'),
        # create below two graphs in one row
        html.Div([
            dcc.Graph(id='device-wise-click'),
            dcc.Graph(id='country-wise-click')
        ], style={'display': 'flex'})        
    ]),
    # create a line here
    html.Hr(),
    # Data without date filter
    html.H2('Top Queries and Pages', style={'text-align': 'center'}),
    html.Hr(),
    dash_table.DataTable(id='top-query', style_cell={'textAlign': 'center', 'margin-bottom': '10px'},
                         style_header={'backgroundColor': 'lightblue'}, style_data={'backgroundColor': 'white'}),
    dash_table.DataTable(id='top-page', style_cell={'textAlign': 'center'}, 
                         style_header={'backgroundColor': 'lightblue'}, style_data={'backgroundColor': 'white'})
    
])    

@app.callback(
    Output('total_clicks_impressions', 'data'),
    Output('overall-traffic', 'figure'),
    Output('day-wise-click', 'figure'),
    Output('device-wise-click', 'figure'),
    Output('country-wise-click', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_overall_traffic(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    filtered_df = dates_df[(dates_df['Date'] >= start_date) & (dates_df['Date'] <= end_date)]
    # click and impression data bs date
    click_data = filtered_df.groupby('Date').sum()['Clicks']
    impression_data = filtered_df.groupby('Date').sum()['Impressions']
    
    total_clicks = click_data.sum()
    total_impressions = impression_data.sum()
    
    # total clicks and impressions table
    data = [{'Total Clicks': total_clicks, 'Total Impressions': total_impressions}]
    
    fig = go.Figure()
    # left y side clicks | right y side impressions
    fig.add_trace(go.Scatter(x=click_data.index, y=click_data, mode='lines', name='Clicks'))
    fig.add_trace(go.Scatter(x=impression_data.index, y=impression_data, mode='lines', name='Impressions', yaxis='y2'))
    fig.update_layout(
        title='Clicks and Impressions Over Time',
        xaxis_title='Date',
        yaxis_title='Clicks (left side)',
        yaxis2=dict(
            title='Impressions (right side)',
            overlaying='y',
            side='right'
        )
    )    
    # groupby on day and sum of clicks
    filtered_df_fig_2 = filtered_df.copy(deep=True)
    filtered_df_fig_2.drop('Date', axis=1, inplace=True)
    filtered_df_fig_2 = filtered_df_fig_2.groupby('Day').sum().reset_index()
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=filtered_df_fig_2['Day'], y=filtered_df_fig_2['Clicks']))
    fig2.update_layout(title='Day Wise Clicks')
    
    # Device wise clicks
    device_clicks = devices_df.groupby('Device').sum()['Clicks']
    fig3 = go.Figure()
    
    fig3.add_trace(go.Pie(labels=device_clicks.index, values=device_clicks))
    fig3.update_layout(title='Device Wise Clicks')
    
    # Country wise clicks
    country_clicks = countries_df.groupby('Country').sum()['Clicks']
    # check top 5 countries with highest clicks
    country_clicks = country_clicks.sort_values(ascending=False).head(5)
    fig4 = go.Figure()
    fig4.add_trace(go.Pie(labels=country_clicks.index, values=country_clicks))
    fig4.update_layout(title='Country Wise Clicks')
    
    # top 5 queries in table format
    top_queries = queries_df.groupby('Top queries').sum().sort_values('Clicks', ascending=False).head(5)
    top_queries = top_queries.reset_index()
    top_queries = top_queries.to_dict('records')
    

    # bar chart for the top 5 pages
    top_pages = pages_df.groupby('Top pages').sum().sort_values('Clicks', ascending=False).head(5)
    top_pages = top_pages.reset_index()
    top_pages = top_pages.to_dict('records')
    
    
    
    return data, fig, fig2, fig3, fig4
    
@app.callback(
    Output('upload-data', 'children'),
    [Input('upload-data', 'filename'),
     Input('upload-data', 'contents')]
)
def update_output(uploaded_filenames, uploaded_file_contents):
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            if name.endswith('.csv'):
                data = data.encode('utf8').split(b';base64,')[1]
                with open(os.path.join(DATA_DIR, name), 'wb') as file:
                    file.write(base64.decodebytes(data))
                    
            elif name.endswith('.zip'):
                data = data.encode('utf8').split(b';base64,')[1]
                with open(os.path.join(DATA_DIR, name), 'wb') as file:
                    file.write(base64.decodebytes(data))
                # unzip the file and save it in the data directory with replacing the existing file
                os.system(f'unzip -o {os.path.join(DATA_DIR, name)} -d {DATA_DIR}')
                
    return [html.Div(['File uploaded successfully!'])]


@app.callback(
    Output('top-query', 'data'),
    Output('top-page', 'data'),
    Input('load_interval', 'n_intervals')
)
def update_top_query_page(n):
    top_queries = queries_df.groupby('Top queries').sum().sort_values('Clicks', ascending=False).head(5)
    top_queries = top_queries.reset_index()
    top_queries = top_queries.to_dict('records')
    
    top_pages = pages_df.groupby('Top pages').sum().sort_values('Clicks', ascending=False).head(5)
    top_pages = top_pages.reset_index()
    top_pages = top_pages.to_dict('records')
    
    return top_queries, top_pages