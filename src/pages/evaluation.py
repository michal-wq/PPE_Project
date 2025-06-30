from typing import List
from dash import html
from src.pages import search
from src import proper_recoomendation
import src.state as state

header = html.Button(
    [
        html.Img(src="./assets/img/Logo.svg", className="search-bar-logo"),
    ],
    id={"type": "nav-button", "route": "home"},
    className="search-bar-container",
)


def get_layout(
    user_inputs: List[str],
    min_rating: float,
    max_rating: float,
):
    proper_recoomendation.get_recommendations(user_inputs, min_rating, max_rating)
    return html.Div(
        [
            header,
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3("All time"),
                                    html.Div(
                                        search.get_films_as_html(
                                            state.recommended_films_all_time,
                                            "evaluation",
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
                                        search.get_films_as_html(
                                            state.recommended_films_classics,
                                            "evaluation",
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
                                        search.get_films_as_html(
                                            state.recommended_films_new_timers,
                                            "evaluation",
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
                className="evaluation-content",
            ),
        ],
    )
