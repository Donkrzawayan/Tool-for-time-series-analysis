import base64
import datetime
import io

import dash
import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import search_methods

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def fun(data, method):
    n_breakpoints = 5
    result = []
    if method == 'NMR':
        result = search_methods.nmr(data, n_breakpoints)
    elif method == 'Dynp':
        result = search_methods.ruptures_dynp(data, n_breakpoints)
    else:
        result = search_methods.ruptures_binseg(data, n_breakpoints)
    fig = px.line(data, title='Chart')
    for changepoint in result:
        fig.add_vline(changepoint)

    return dcc.Graph(
        id='line-graph',
        figure=fig
    )


app.layout = html.Div([
    html.H1(
        'Tool for time series analysis',
        style={
            'textAlign': 'center'
        }
    ),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Quality Control Procedure Based on Partitioning of NMR Time Series', 'value': 'NMR'},
            {'label': 'ruptures Dynp', 'value': 'Dynp'},
            {'label': 'ruptures Binseg', 'value': 'Binseg'}
        ],
        value='NMR'
    ),

    html.Div(id='output-data-upload'),
])


def parse_contents(method, contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        fun(np.array(df['TOBS']), method),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('dropdown', 'value'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(method, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(method, c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


if __name__ == '__main__':
    app.run_server(debug=True)
