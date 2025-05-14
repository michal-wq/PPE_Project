from dash import html, dcc
import pandas as pd

search_bar = html.Div(
    [
        html.Img(src="./assets/img/Logo.svg", className="search-bar-logo"),
        html.Div(
            [
                dcc.Input("", placeholder="Search...", id="search-bar-input"),
                html.Button(html.Img(src="./assets/icons/search.svg")),
            ],
            className="search-bar-field",
        ),
    ],
    className="search-bar-container",
)

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

big_list = html.Div([big_list_item for i in range(1, 10)], className="big-list")

small_list_item = html.Div("dobar dan")

layout = html.Div([search_bar, big_list])


def get_layout():
    return layout


def get_random_movies(number):
    df_movies = pd.read_csv("../../Data/raw/movies.csv")
    df_links = pd.read_csv("../../Data/raw/links.csv")
    merged_df = pd.merge(df_movies, df_links, on="movieId")
    pass
