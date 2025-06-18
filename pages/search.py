from __future__ import annotations
from dash import ctx, html, dcc, Dash
from dash.dependencies import Output, Input, State, ALL
import pandas as pd
from typing import List, Union, Optional, Any


# Film class, which will be used for
class Film:
    def __init__(
        self, movie_id: str, imdb_id: str, title: str, release_year: int, genres: str
    ) -> None:
        self.movie_id: str = movie_id
        self.imdb_id: str = imdb_id
        self.title: str = title
        self.release_year: int = release_year
        self.genres: List[str] = genres.split("|")


# Instancing necessary
all_films_cache: List[Film] = []
shown_films_cache: List[Film] = []
selected_films_cache: List[Film] = []


def update_all_films_cache():
    global all_films_cache, shown_films_cache

    existing_ids = {film.movie_id for film in all_films_cache}

    for film in shown_films_cache:
        if film.movie_id not in existing_ids:
            all_films_cache.append(film)
            existing_ids.add(film.movie_id)


def get_random_films(number: Optional[int]) -> List[Film]:
    films_list: List[Film] = []

    if number is None or number < 1:
        return films_list

    df_movies: pd.DataFrame = pd.read_csv("./Data/raw/movies.csv")
    df_links: pd.DataFrame = pd.read_csv("./Data/raw/links.csv")

    merged_df = pd.merge(df_movies, df_links, on="movieId")
    merged_df.drop(columns=["tmdbId"], inplace=True)
    merged_df["year"] = merged_df["title"].str.extract(r"\((\d{4})\)")
    merged_df["title"] = merged_df["title"].str.replace(
        r"\s*\(\d{4}\)\s*", "", regex=True
    )

    subset_df: pd.DataFrame = merged_df.sample(n=number)

    for _, row in subset_df.iterrows():
        year_str: str = str(row["year"]) if pd.notna(row["year"]) else "0"
        try:
            release_year: int = int(year_str) if year_str.isdigit() else 0
        except ValueError:
            release_year = 0

        film = Film(
            movie_id=str(row["movieId"]),
            imdb_id=str(row["imdbId"]),
            title=str(row["title"]),
            release_year=release_year,
            genres=str(row["genres"]),
        )
        films_list.append(film)

    global shown_films_cache
    shown_films_cache = films_list
    update_all_films_cache()

    return films_list


def get_films_by_title(title_query: str) -> List[Film]:
    films_list: List[Film] = []

    if not title_query or len(title_query.strip()) == 0:
        return films_list

    df_movies = pd.read_csv("./Data/raw/movies.csv")
    df_links = pd.read_csv("./Data/raw/links.csv")

    merged_df = pd.merge(df_movies, df_links, on="movieId")
    merged_df.drop(columns=["tmdbId"], inplace=True)
    merged_df["year"] = merged_df["title"].str.extract(r"\((\d{4})\)")
    merged_df["title"] = merged_df["title"].str.replace(
        r"\s*\(\d{4}\)\s*", "", regex=True
    )

    subset_df = merged_df[
        merged_df["title"].str.contains(title_query, case=False, na=False)
    ]

    for _, row in subset_df.iterrows():
        year_str: str = str(row["year"]) if pd.notna(row["year"]) else "0"
        try:
            release_year: int = int(year_str) if year_str.isdigit() else 0
        except ValueError:
            release_year = 0

        film = Film(
            movie_id=str(row["movieId"]),
            imdb_id=str(row["imdbId"]),
            title=str(row["title"]),
            release_year=release_year,
            genres=str(row["genres"]),
        )
        films_list.append(film)

    global shown_films_cache
    shown_films_cache = films_list
    update_all_films_cache()

    return films_list


def get_film_as_html(film_list: List[Film], mode="search") -> Optional[List[html.Div]]:
    if not film_list:
        return None

    return [
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
                        html.H5(str(film.release_year), className="big-list-item-year"),
                    ],
                    className="big-list-item-title-year",
                ),
                (
                    html.Button(
                        [
                            html.Img(src="../assets/icons/add-circle.svg"),
                            "Add to liked films",
                        ],
                        className="big-list-item-add-to-liked-films-button",
                        id={"type": "add-to-liked-button", "id": film.movie_id},
                        n_clicks=0,
                    )
                    if mode == "search"
                    else None
                ),
            ],
            className="big-list-item",
        )
        for film in film_list
    ]


search_bar: html.Div = html.Div(
    [
        html.Img(src="./assets/img/Logo.svg", className="search-bar-logo"),
        html.Div(
            [
                dcc.Input(
                    id="search-bar-input",
                    type="text",
                    placeholder="Search...",
                    value="",
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

liked_films: html.Div = html.Div(
    len(selected_films_cache),
    className="liked-films-container",
    id="liked-films-container",
)


def get_layout() -> html.Div:
    global shown_films_cache
    shown_films_cache = get_random_films(15)
    update_all_films_cache()

    big_list: html.Div = html.Div(
        get_film_as_html(shown_films_cache), className="big-list", id="big-list"
    )
    liked_films_container: html.Div = html.Div(id="liked-films-container")

    return html.Div([search_bar, big_list, liked_films_container])


def register_callbacks(app: Dash) -> None:
    @app.callback(
        Output("big-list", "children"),
        [Input("search-button", "n_clicks")],
        [Input("search-bar-input", "value")],
    )
    def perform_search(
        n_clicks: Optional[int], search_value: str
    ) -> Union[List[html.Div], None]:
        global shown_films_cache

        if not n_clicks:
            return get_film_as_html(shown_films_cache)

        if not search_value:
            return [
                html.Div("Enter a search query to find movies.", className="no-results")
            ]

        films = get_films_by_title(search_value)

        if films:
            return get_film_as_html(films)

        return [html.Div("No movies found.", className="no-results")]

    @app.callback(
        Output("liked-films-container", "children"),
        [Input({"type": "add-to-liked-button", "id": ALL}, "n_clicks")],
        [State({"type": "add-to-liked-button", "id": ALL}, "id")],
    )
    def add_to_liked_films(
        n_clicks: List[int], button_ids: List[dict[str, Any]]
    ) -> html.Div:

        triggered = ctx.triggered_id

        global all_films_cache, shown_films_cache, selected_films_cache

        selected_films_ids = {film.movie_id for film in selected_films_cache}

        for n_click, button_id in zip(n_clicks, button_ids):
            selected_film = next(
                (
                    film
                    for film in all_films_cache
                    if film.movie_id == button_id.get("id")
                ),
                None,
            )

            selected_film_id = (
                selected_film.movie_id if selected_film is not None else ""
            )

            if (
                (n_click != 0 or n_click is not None)
                and n_click % 2 == 1
                and selected_film is not None
                and selected_film_id not in selected_films_ids
            ):
                selected_films_cache.append(selected_film)

            elif (
                (n_click != 0 or n_click is not None)
                and n_click % 2 == 0
                and selected_film_id in selected_films_ids
            ):
                film_to_deselect = next(
                    (
                        film
                        for film in selected_films_cache
                        if film.movie_id == selected_film_id
                    ),
                    None,
                )
                if film_to_deselect is not None:
                    selected_films_cache.remove(film_to_deselect)

        return html.Div(
            [
                html.Div(
                    [html.Div(film.title) for film in selected_films_cache] or " "
                ),
                html.Button(
                    [
                        html.Img(src="../assets/icons/done.svg"),
                        "evaluate shiiii",
                    ],
                    className="eval-button button-primary",
                    id={"type": "nav-button", "route": "evaluation"},
                    n_clicks=0,
                ),
            ],
            className="footer-eval-container",
        )
