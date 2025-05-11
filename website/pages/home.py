from dash import html

layout = html.Div(
    [
        html.Img(src="./assets/img/Logo + Title.svg"),
        html.Div(
            [
                html.Button(
                    "Find the perfect match",
                    className="button-primary",
                    id="change-search-view",
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
