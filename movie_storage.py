import json
import requests
from storage_json import StorageJson


# Constants to remain while there is the use of API https://www.omdbapi.com/
URL_API = "http://www.omdbapi.com/"
API_KEY = "c3bb5c1c"
JSON_FILE = 'data.json'

storage = StorageJson(JSON_FILE)


def add_movie(movie_title):
    """
    Adds a movie to the movies database.
    Loads the information from the api , add the movie,
    and saves it.
    """
    movies = storage.list_movies()
    if movie_title in movies:
        print(f"Movie '{movie_title}' already exists!")
        return

    # add the api call
    url = f'{URL_API}?t={movie_title}&apikey={API_KEY}'
    response = requests.get(url)

    # error handling begins with check for correct status code
    if response.status_code != 200:
        print("Failed to fetch data from the API")
        return

    movie_data = response.json()

    # check if the movie exists
    if movie_data.get("Response") == "False":
        print(f"Movie '{movie_title}' not found!")
        return

    title = movie_data.get("Title", "N/A")
    year = movie_data.get("Year", "N/A")
    rating = movie_data.get("imdbRating", "N/A")
    poster = movie_data.get("Poster", "N/A")

    movies[title] = {
        "Title": movie_title,
        "year": year,
        "rating": rating,
        "poster": poster
    }

    storage.add_movie(title, year, rating, poster)
    print(f"Movie '{title}' added successfully!")


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    """
    storage.delete_movie(title)


def update_movie(movie_title, new_rating):
    """
    Updates the rating of a movie in the movies database using the storage class.
    """
    movies = storage.list_movies()
    movie_title_lower = movie_title.lower()  # Convert input title to lowercase

    if movie_title_lower in movies:
        storage.update_movie(movie_title_lower, new_rating)  # Use lowercase title for update
        print(f"Movie '{movie_title}' rating updated to {new_rating}")
    else:
        print(f"The movie '{movie_title}' is not in the database.")

def list_movies():
    """
    Returns a dictionary of dictionaries that contains the movies information in the database.
    """
    return storage.list_movies()
