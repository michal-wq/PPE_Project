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


# Register the callback
def register_callbacks(app):
    @app.callback(
        Output("app-content", "children"),
        Input("change-search-view", "n_clicks"),
    )
    def change_page(change_to_search_view):
        if change_to_search_view < 1:
            return get_layout()

        return search.get_layout()
