from dash import html, dcc, Dash
from dash.dependencies import Output, Input, State, ALL
import pandas as pd
import src.state as state


def get_layout():
    return html.Div("MEOW")
