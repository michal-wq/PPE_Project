from dash import html

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
                html.Button(
                    "Visualisation",
                    className="button-secondary",
                    id={"type": "nav-button", "route": "visualisation"},
                ),
                html.Button(
                    "Imprint",
                    className="button-secondary",
                    id={"type": "nav-button", "route": "imprint"},
                ),
            ],
            className="homepage-button-container",
        ),
    ],
    className="homepage-content",
)


def get_layout():
    return layout
