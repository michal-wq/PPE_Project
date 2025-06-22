# Global vars
from typing import List


# Film class
class Film:
    def __init__(
        self, movie_id: str, imdb_id: str, title: str, release_year: int, genres: str
    ) -> None:
        self.movie_id: str = movie_id
        self.imdb_id: str = imdb_id
        self.title: str = title
        self.release_year: int = release_year
        self.genres: List[str] = genres.split("|")


# Search page vars
all_films_cache: List[Film] = []
shown_films_cache: List[Film] = []
selected_films_cache: List[Film] = []


def reset_page_vars():
    global all_films_cache, shown_films_cache, selected_films_cache
    all_films_cache = []
    shown_films_cache = []
    selected_films_cache = []


# Evaluation vars
user_inputs: List[str] = []
min_rating: float = 0.0
max_rating: float = 5.0


recommended_films_all_time: List[Film] = []
recommended_films_classics: List[Film] = []
recommended_films_new_timers: List[Film] = []


def reset_evaluation_vars():
    global user_inputs
    user_inputs = []
