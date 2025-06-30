from dash import html, dcc, Dash
from dash.dependencies import Output, Input, State, ALL
import pandas as pd
import src.state as state
from typing import List, Union, Optional, Any


def update_all_films_cache():
    existing_ids = {film.movie_id for film in state.all_films_cache}

    for film in state.shown_films_cache:
        if film.movie_id not in existing_ids:
            state.all_films_cache.append(film)
            existing_ids.add(film.movie_id)


def get_random_films(number: Optional[int]) -> List[state.Film]:
    films_list: List[state.Film] = []

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

        film = state.Film(
            movie_id=str(row["movieId"]),
            imdb_id=str(row["imdbId"]),
            title=str(row["title"]),
            release_year=release_year,
            genres=str(row["genres"]),
        )
        films_list.append(film)
    state.shown_films_cache = films_list
    update_all_films_cache()

    return films_list


def get_films_by_title(title_query: str) -> List[state.Film]:
    films_list: List[state.Film] = []

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

        film = state.Film(
            movie_id=str(row["movieId"]),
            imdb_id=str(row["imdbId"]),
            title=str(row["title"]),
            release_year=release_year,
            genres=str(row["genres"]),
        )
        films_list.append(film)
    state.shown_films_cache = films_list
    update_all_films_cache()

    return films_list


def get_films_as_html(film_list: List[state.Film], mode="search"):
    if not film_list:
        return None

    return [
        html.Div(
            [
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
                            html.Div(
                                [
                                    html.Img(src="../assets/icons/add-circle.svg"),
                                    "Add to liked films",
                                ],
                                className="add-to-liked-films-label",
                            ),
                            html.Div("Deselect", className="deselect-label"),
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
        html.Button(
            html.Img(src="./assets/img/Logo.svg", className="search-bar-logo"),
            id={"type": "nav-button", "route": "home"},
        ),
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
    len(state.selected_films_cache),
    className="liked-films-container",
    id="liked-films-container",
)


def get_layout() -> html.Div:
    state.shown_films_cache = get_random_films(30)
    update_all_films_cache()

    big_list: html.Div = html.Div(
        get_films_as_html(state.shown_films_cache), className="big-list", id="big-list"
    )
    liked_films_container: html.Div = html.Div(id="liked-films-container")

    return html.Div(
        [
            search_bar,
            big_list,
            liked_films_container,
        ]
    )


def register_callbacks(app: Dash) -> None:
    @app.callback(
        Output("big-list", "children"),
        [Input("search-button", "n_clicks")],
        [Input("search-bar-input", "value")],
    )
    def perform_search(
        n_clicks: Optional[int], search_value: str
    ) -> Union[List[html.Div], None]:

        if not n_clicks:
            return get_films_as_html(state.shown_films_cache)

        if not search_value:
            state.shown_films_cache = get_random_films(30)
            update_all_films_cache()
            return get_films_as_html(state.shown_films_cache)

        films = get_films_by_title(search_value)

        if films:
            return get_films_as_html(films)

        return [html.Div("No movies found.", className="no-results")]

    @app.callback(
        [
            Output("liked-films-container", "children"),
            Output({"type": "add-to-liked-button", "id": ALL}, "className"),
        ],
        [Input({"type": "add-to-liked-button", "id": ALL}, "n_clicks")],
        [State({"type": "add-to-liked-button", "id": ALL}, "id")],
    )
    def add_to_liked_films(n_clicks: List[int], button_ids: List[dict[str, Any]]):
        selected_films_ids = {film.movie_id for film in state.selected_films_cache}

        for n_click, button_id in zip(n_clicks, button_ids):
            selected_film = next(
                (
                    film
                    for film in state.all_films_cache
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
                state.selected_films_cache.append(selected_film)

            elif (
                (n_click != 0 or n_click is not None)
                and n_click % 2 == 0
                and selected_film_id in selected_films_ids
            ):
                film_to_deselect = next(
                    (
                        film
                        for film in state.selected_films_cache
                        if film.movie_id == selected_film_id
                    ),
                    None,
                )
                if film_to_deselect is not None:
                    state.selected_films_cache.remove(film_to_deselect)

            state.user_inputs = [i.title for i in state.selected_films_cache]

        button_classes = []

        for button_id in button_ids:
            movie_id = button_id.get("id")
            is_selected = any(
                f.movie_id == movie_id for f in state.selected_films_cache
            )
            if is_selected:
                button_classes.append("big-list-item-add-to-liked-films-button-bruh")
            else:
                button_classes.append("big-list-item-add-to-liked-films-button")

        return [
            html.Div(
                [
                    html.Div(
                        f"You've selected this many films: {len(state.selected_films_cache)}",
                    ),
                    html.Button(
                        [
                            html.Img(src="../assets/icons/done.svg"),
                            "Recommend me films",
                        ],
                        className=(
                            "button-primary eval-button"
                            + (
                                " disabled-eval-button"
                                if len(state.selected_films_cache) < 3
                                else ""
                            )
                        ),
                        id={"type": "nav-button", "route": "evaluation"},
                        n_clicks=0,
                        disabled=len(state.selected_films_cache) < 3,
                    ),
                ],
                className="footer-eval-container",
            ),
            button_classes,
        ]
