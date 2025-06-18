from typing import List
from dash import html
from pages import search


from pages.search import Film

# Recommended film lists (mock data)
recommended_films_all_time: List[Film] = [
    Film("1", "tt0111161", "The Shawshank Redemption", 1994, "Drama|Crime"),
    Film("2", "tt0068646", "The Godfather", 1972, "Crime|Drama"),
    Film("3", "tt0071562", "The Godfather: Part II", 1974, "Crime|Drama"),
    Film("4", "tt0468569", "The Dark Knight", 2008, "Action|Crime|Drama"),
    Film("5", "tt0050083", "12 Angry Men", 1957, "Drama"),
]

recommended_films_classics: List[Film] = [
    Film("6", "tt0108052", "Schindler's List", 1993, "Biography|Drama|History"),
    Film(
        "7",
        "tt0167260",
        "The Lord of the Rings: The Return of the King",
        2003,
        "Adventure|Drama|Fantasy",
    ),
    Film("8", "tt0110912", "Pulp Fiction", 1994, "Crime|Drama"),
    Film("9", "tt0060196", "The Good, the Bad and the Ugly", 1966, "Western"),
    Film("10", "tt0137523", "Fight Club", 1999, "Drama"),
]

recommended_films_new_timers: List[Film] = [
    Film("11", "tt4154796", "Avengers: Endgame", 2019, "Action|Adventure|Drama"),
    Film("12", "tt6723592", "Tenet", 2020, "Action|Sci-Fi|Thriller"),
    Film("13", "tt1375666", "Inception", 2010, "Action|Adventure|Sci-Fi"),
    Film("14", "tt2948372", "Soul", 2020, "Animation|Adventure|Comedy"),
    Film("15", "tt10648342", "The Father", 2020, "Drama"),
]

layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H3("All time"),
                        html.Div(
                            search.get_film_as_html(
                                recommended_films_all_time, "evaluation"
                            )
                            or [],
                            className="recommendation-category-list",
                        ),
                    ],
                    className="recommendation-category",
                ),
                html.Div(
                    [
                        html.H3("Classics"),
                        html.Div(
                            search.get_film_as_html(
                                recommended_films_classics, "evaluation"
                            )
                            or [],
                            className="recommendation-category-list",
                        ),
                    ],
                    className="recommendation-category",
                ),
                html.Div(
                    [
                        html.H3("New timers"),
                        html.Div(
                            search.get_film_as_html(
                                recommended_films_new_timers, "evaluation"
                            )
                            or [],
                            className="recommendation-category-list",
                        ),
                    ],
                    className="recommendation-category",
                ),
            ],
            className="recommendations",
        ),
        html.Div(
            [
                html.Button(
                    "Retry",
                    className="retry-button",
                    id={"type": "nav-button", "route": "search"},
                ),
                html.Button(
                    "Home",
                    className="home-button",
                    id={"type": "nav-button", "route": "home"},
                ),
            ],
            className="retry-home-buttons",
        ),
    ],
    className="homepage-content",
)


def get_layout():
    return layout
