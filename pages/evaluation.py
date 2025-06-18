from dash import html
from dash.dependencies import Output, Input
from pages import search


layout = html.Div(
    [
        html.Div(
            [
                html.Div([html.Div(["All time", html.Div([])])]),
                html.Div([html.Div(["Classics", html.Div([])])]),
                html.Div([html.Div(["New timers", html.Div([])])]),
            ],
            className="recommendations",
        ),
        html.Div(
            [
                html.Button(
                    "Retry",
                    className="retry-button",
                    id={"type": "nav-button", "route": "search"},
                ),
                html.Button(
                    "Home",
                    className="home-button",
                    id={"type": "nav-button", "route": "home"},
                ),
            ],
            className="retry-home-buttons",
        ),
    ],
    className="homepage-content",
)


def get_layout():
    return layout
