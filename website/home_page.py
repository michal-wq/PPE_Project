from dash import Dash, html, dcc

layout = html.Div(
    [
        html.Img(src="./assets/img/Logo + Title.svg"),
        html.Div(
            [
                html.Button("Find the perfect match", className="button-primary"),
                html.Button("Imprint", className="button-secondary"),
            ],
            className="homepage-button-container",
        ),
    ],
    className="homepage-content",
)
