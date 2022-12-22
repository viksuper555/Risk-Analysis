
import plotly.graph_objects as go
import tree
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import dash_table
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
from dash_table.Format import Format, Scheme

elements = tree.get_nodes() + tree.get_edges()
params = [
    ('v1', ['V', 'v1']),
    ('v2', ['V', 'v2']),
    ('pti', ['', 'P(ϑ)']),
    ('ε1', ['p(ε|ϑ)', 'ε1']),
    ('ε2', ['p(ε|ϑ)', 'ε2']),
    ('ε3', ['p(ε|ϑ)', 'ε3']),
]

def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Clinical Analytics"),
            html.H3("Welcome to the Clinical Analytics Dashboard"),
            html.Div(
                id="intro",
                children="Explore clinic patient volume by time of day, waiting time, and care score. Click on the heatmap to visualize patient experience at different time points.",
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for input data.
    """

    return html.Div(
        id="control-card",
        children=[
            dbc.Label("Input data"),
            dash_table.DataTable(
                id='table-input',
                columns=(
                    [{'id': 'ti', 'name': ['', 'ϑ'], 'editable':False}] +
                    [{'id': p[0], 'name': p[1], 'type': 'numeric'} for p in params]
                ),
                data=[
                    dict(ti=f'ϑ{i}', **{param[0]: 0 for param in params})
                    for i in range(1, 5)
                ],
                css=[
                {"selector": ".column-header--delete svg", "rule": 'display: "none"'},
                {"selector": ".column-header--delete::before", "rule": 'content: "X"'}
                ],
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                editable=True,
                merge_duplicate_headers=True
            ),
            html.Br(),
            html.Div(
                dbc.Button("Generate", id="generate-btn", size="lg", color="success", n_clicks=0),
                id="generate-btn-outer"
            ),
        ],
    )


def generate_results():
    return html.Div([ 
    dash_table.DataTable(
        id='table-results'
    ),
    cyto.Cytoscape(
        id='cytoscape-layout',
        layout={'name': 'grid'},
        style={'width': '100%', 'height': '450px'},
        elements=elements
    )])