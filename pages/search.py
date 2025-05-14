from dash import html, dcc
import pandas as pd


class Film:
    def __init__(self, movie_id, imdb_id, title, release_year, genres):
        self.movie_id = movie_id
        self.imdb_id = imdb_id
        self.title = title
        self.release_year = release_year
        self.genres = genres.split("|")


def get_random_films(number):
    films_list = []

    if number is None:
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

    for film in films_list:
        print(f"Title: {film.title}, Year: {film.release_year}, Genres: {film.genres}")

    return films_list


def get_film_as_html(film_list):
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


def get_layout():
    big_list = html.Div(get_film_as_html(get_random_films(15)), className="big-list")
    layout = html.Div([search_bar, big_list])
    return layout
