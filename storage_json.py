from istorage import IStorage
import json
import requests

# Constants to remain while there is the use of API https://www.omdbapi.com/
URL_API = "http://www.omdbapi.com/"
API_KEY = "c3bb5c1c"
JSON_FILE = 'data.json'

class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def _read_storage(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _write_storage(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)


    def list_movies(self):
        return self._read_storage()


    def add_movie(self, title, year, rating, poster):
        """
            Adds a movie to the movies database.
            Loads the information from the api , add the movie,
            and saves it.
            """
        movies = self.list_movies()
        if title in movies:
            print(f"Movie '{title}' already exists!")
            return

        # add the api call
        url = f'{URL_API}?t={title}&apikey={API_KEY}'
        response = requests.get(url)

        movie_data = response.json()

        # check if the movie exists
        if movie_data.get("Response") == "False":
            print(f"Movie '{title}' not found!")
            return

        title = movie_data.get("Title", "N/A")
        year = movie_data.get("Year", "N/A")
        rating = movie_data.get("imdbRating", "N/A")
        poster = movie_data.get("Poster", "N/A")

        movies[title] = {
            "Title": title,
            "year": year,
            "rating": rating,
            "poster": poster
        }

        self._save_movies(movies)
        print(f"Movie '{title}' added successfully!")

    def delete_movie(self, title):
        movies = self.list_movies()
        lowercase_titles = {key.lower(): key for key in movies.keys()}

        if title.lower() in lowercase_titles:
            original_title = lowercase_titles[title.lower()]  # Get the original case title
            del movies[original_title]
            self._save_movies(movies)
            print(f"Movie '{original_title}' has been deleted.")
            return True
        else:
            print(f"Movie '{title}' is not in the database.")
            return False


    def update_movie(self, title, new_rating):
        movies = self.list_movies()
        lowercase_titles = {key.lower(): key for key in movies.keys()}

        if title.lower() in lowercase_titles:
            original_title = lowercase_titles[title.lower()]  # Get the original case title
            movies[original_title]["rating"] = new_rating
            self._save_movies(movies)  # Save the updated movies dictionary
            print(f"Movie '{original_title}' rating updated to {new_rating}")
            return True
        else:
            print(f"The movie '{title}' is not in the database.")
            return False

    def _save_movies(self, movies):
        with open(self.file_path, 'w', encoding="utf-8") as handle:
            json.dump(movies, handle, indent=4)