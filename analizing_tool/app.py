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
import random_time_series as rts

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def fun(data, method):
    n_breakpoints = 5

    fig = px.line(data)

    if 'NMR' in method:
        result = search_methods.nmr(data, n_breakpoints)
        for changepoint in result:
            fig.add_vline(changepoint, line_color='black', annotation_text='NMR')
            fig.update_layout(  # annotation in the middle
                annotations=[{**a, **{"y": .5}} for a in fig.to_dict()["layout"]["annotations"]]
            )
    if 'Dynp' in method:
        result = search_methods.ruptures_dynp(data, n_breakpoints)
        for changepoint in result:
            fig.add_vline(changepoint, line_color='green', annotation_text='Dynp', annotation_position='top right')
    if 'Binseg' in method:
        result = search_methods.ruptures_binseg(data, n_breakpoints)
        for changepoint in result:
            fig.add_vline(changepoint, line_color='blue', annotation_text='Binseg', annotation_position='bottom right')

    fig.update_layout(showlegend=False)
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
            html.A('Select CSV File')
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
    html.Div([
        html.Label(
            'Enter column index: ',
            style={
                'display': 'inline-block',
                'marginRight': 10
            }),
        dcc.Input(id='csv_index', type='number', min=0),
    ], style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Quality Control Procedure Based on Partitioning of NMR Time Series', 'value': 'NMR'},
            {'label': 'ruptures Dynp', 'value': 'Dynp'},
            {'label': 'ruptures Binseg', 'value': 'Binseg'}
        ],
        value=['NMR'],
        multi=True
    ),

    html.Div(id='output-data-upload'),
])


def parse_contents(method, csv_index, contents, filename, date):
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

    csv_index = 0 if csv_index is None else csv_index

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        fun(np.array(df.iloc[:, csv_index]), method),

        html.Hr(),  # horizontal line
    ])


def parse_random(method):
    data_points, n_breakpoints, snr = 100, 5, 30
    df, breakpoints = rts.gen_rand(data_points, n_breakpoints, snr)

    return html.Div([
        html.H5('Random data'),
        html.H6(datetime.datetime.now()),

        fun(np.array(df), method),

        html.Hr(),  # horizontal line
    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('dropdown', 'value'),
              Input('csv_index', 'value'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(method, csv_index, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(method, csv_index, c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    else:
        return [parse_random(method)]


if __name__ == '__main__':
    app.run_server(debug=False)
