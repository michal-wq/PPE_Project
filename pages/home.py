from dash import html
from dash.dependencies import Output, Input
from pages import search

layout = html.Div(
    [
        html.Img(src="./assets/img/Logo + Title.svg"),
        html.Div(
            [
                html.Button(
                    "Find the perfect match",
                    className="button-primary",
                    id={"type": "nav-button", "route": "search"},
                    n_clicks=0,
                ),
                html.Button("Imprint", className="button-secondary"),
            ],
            className="homepage-button-container",
        ),
    ],
    className="homepage-content",
)


def get_layout():
    return layout
