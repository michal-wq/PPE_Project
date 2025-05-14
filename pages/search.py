from dash import html, dcc
from dash.dependencies import Output, Input
import pandas as pd


class Film:
    def __init__(self, movie_id, imdb_id, title, release_year, genres):
        self.movie_id = movie_id
        self.imdb_id = imdb_id
        self.title = title
        self.release_year = release_year
        self.genres = genres.split("|")


film_cache = []


def get_random_films(number):
    films_list = []

    if number is None or number < 1:
        return films_list

    df_movies = pd.read_csv("./Data/raw/movies.csv")
    df_links = pd.read_csv("./Data/raw/links.csv")

    merged_df = pd.merge(df_movies, df_links, on="movieId")
    merged_df.drop(columns=["tmdbId"], inplace=True)
    merged_df["year"] = merged_df["title"].str.extract(r"\((\d{4})\)")
    merged_df["title"] = merged_df["title"].str.replace(
        r"\s*\(\d{4}\)\s*", "", regex=True
    )

    subset_df = merged_df.sample(number)

    for index, row in subset_df.iterrows():
        film = Film(
            row["movieId"], row["imdbId"], row["title"], row["year"], row["genres"]
        )
        films_list.append(film)

    global film_cache
    film_cache = films_list

    return films_list


def get_films_by_title(title_query):
    films_list = []

    # If the query is None or empty, return an empty list
    if not title_query or len(title_query.strip()) == 0:
        return films_list

    # Read the CSV files
    df_movies = pd.read_csv("./Data/raw/movies.csv")
    df_links = pd.read_csv("./Data/raw/links.csv")

    # Merge the two DataFrames
    merged_df = pd.merge(df_movies, df_links, on="movieId")
    merged_df.drop(columns=["tmdbId"], inplace=True)

    # Extract the year and clean the title
    merged_df["year"] = merged_df["title"].str.extract(r"\((\d{4})\)")
    merged_df["title"] = merged_df["title"].str.replace(
        r"\s*\(\d{4}\)\s*", "", regex=True
    )

    # 🔍 **Filter by the search query (case-insensitive)**
    subset_df = merged_df[
        merged_df["title"].str.contains(title_query, case=False, na=False)
    ]

    # Build the list of Film objects
    for _, row in subset_df.iterrows():
        film = Film(
            row["movieId"], row["imdbId"], row["title"], row["year"], row["genres"]
        )
        films_list.append(film)

    # Update the global cache
    global film_cache
    film_cache = films_list

    return films_list


def get_film_as_html(film_list):
    if not film_list:
        return None

    html_list = [
        html.Div(
            [
                html.Div(None, className="big-list-item-preview-pic"),
                html.Div(
                    [
                        html.Div(genre, className="big-list-item-genre-chip")
                        for genre in film.genres
                    ],
                    className="big-list-item-genre-chips",
                ),
                html.Div(
                    [
                        html.H3(film.title, className="big-list-item-title"),
                        html.H5(film.release_year, className="big-list-item-year"),
                    ],
                    className="big-list-item-title-year",
                ),
                html.Button(
                    [
                        html.Img(src="../assets/icons/add-circle.svg"),
                        "Add to liked films",
                    ],
                    className="big-list-item-add-to-liked-films-button",
                ),
            ],
            className="big-list-item",
        )
        for film in film_list
    ]
    return html_list


# The search bar component
search_bar = html.Div(
    [
        html.Img(src="./assets/img/Logo.svg", className="search-bar-logo"),
        html.Div(
            [
                dcc.Input(
                    id="search-bar-input",
                    type="text",
                    placeholder="Search...",
                    value="",  # <-- Ensure it is initialized as an empty string
                    debounce=True,
                ),
                html.Button(
                    html.Img(src="./assets/icons/search.svg"),
                    id="search-button",
                    n_clicks=0,
                ),
            ],
            className="search-bar-field",
        ),
    ],
    className="search-bar-container",
)


# Main layout for the search page
def get_layout():
    global film_cache
    film_cache = get_random_films(15)
    big_list = html.Div(
        get_film_as_html(film_cache), className="big-list", id="big-list"
    )
    return html.Div([search_bar, big_list])


# 🔥 Register Callbacks
def register_callbacks(app):

    @app.callback(
        Output("big-list", "children"),
        [Input("search-button", "n_clicks")],
        [Input("search-bar-input", "value")],
    )
    def perform_search(n_clicks, search_value):
        if n_clicks is None or n_clicks == 0:
            global film_cache
            return get_film_as_html(film_cache)

        if not search_value:
            return [
                html.Div("Enter a search query to find movies.", className="no-results")
            ]

        films = get_films_by_title(search_value)

        if films:
            print(f"Found {len(films)} movies.")
            return get_film_as_html(films)
        else:
            print("No movies found.")
            return [html.Div("No movies found.", className="no-results")]
