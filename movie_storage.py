import json
import requests

# Constants to remain while there is the use of API https://www.omdbapi.com/
URL_API = "http://www.omdbapi.com/"
API_KEY = "c3bb5c1c"
JSON_FILE = 'data.json'


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.
    The function loads the information from the JSON
    file and returns the data.
    """
    try:
        with open(JSON_FILE, 'r') as handle:
            movies_data = json.load(handle)
        return movies_data
    except FileNotFoundError:
        return {}


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open(JSON_FILE, 'w') as handle:
        json.dump(movies, handle, indent=4)


def add_movie(movie_title):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
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

    save_movies(movies)
    print(f"Movie '{title}' added successfully!")


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    found = False

    # Convert movie titles to lowercase for case-insensitive comparison
    lowercase_titles = {key.lower(): key for key in movies.keys()}

    if title.lower() in lowercase_titles:
        title = lowercase_titles[title.lower()]  # Get the original case title
        del movies[title]
        save_movies(movies)
        found = True
    else:
        print(f"Movie '{title}' is not in the database.")

    return found


def update_movie(movie_title, new_rating):
    """
    Updates the rating of a movie in the movies database.
    Loads the information from the JSON file, updates the movie, and saves it.
    """
    movies = get_movies()
    if movie_title in movies:
        movies[movie_title]["rating"] = new_rating
        save_movies(movies)
        print(f"Movie '{movie_title}' rating updated to {new_rating}")
    else:
        print(f"The movie '{movie_title}' is not in the database.")