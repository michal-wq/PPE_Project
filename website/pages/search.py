from dash import Dash, html, dcc


big_list_item = html.Div(
    [
        html.Div(None, className="big-list-item-preview-pic"),
        html.Div(
            [
                html.Div("Action", className="big-list-item-genre-chip"),
                html.Div("Crime", className="big-list-item-genre-chip"),
                html.Div("Thriller", className="big-list-item-genre-chip"),
            ],
            className="big-list-item-genre-chips",
        ),
        html.Div(
            [
                html.H3("The fast and the furious", className="big-list-item-title"),
                html.H5("2001", className="big-list-item-year"),
            ],
            className="big-list-item-title-year",
        ),
        html.Button(
            [html.Img(src="../assets/icons/add-circle.svg"), "Add to liked films"],
            className="big-list-item-add-to-liked-films-button",
        ),
    ],
    className="big-list-item",
)

small_list_item = html.Div("dobar dan")


layout = html.Div([big_list_item])


def get_layout():
    return layout
