from istorage import IStorage
import requests
import csv

# Constants for the OMDB API
URL_API = "http://www.omdbapi.com/"
API_KEY = "c3bb5c1c"

class StorageCsv(IStorage):

    def __init__(self, file_path):
        self.file_path = file_path

    def _read_storage(self):
        movies = {}
        try:
            with open(self.file_path, 'r', newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row['title']
                    movies[title] = {
                        "year": row['year'],
                        "rating": row['rating'],
                        "poster": row['poster']
                    }
        except FileNotFoundError:
            pass
        return movies

    def _write_storage(self, movies):
        with open(self.file_path, 'w', newline='', encoding="utf-8") as file:
            fieldnames = ["title", "year", "rating", "poster"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                row = {"title": title, **details}
                writer.writerow(row)

    def list_movies(self):
        return self._read_storage()

    def add_movie(self, title, year=None, rating=None, poster=None):
        """
        Adds a movie to the movies database.
        Loads the information from the API, adds the movie, and saves it.
        """
        movies = self.list_movies()
        if title in movies:
            print(f"Movie '{title}' already exists!")
            return

        # Add the API call
        url = f'{URL_API}?t={title}&apikey={API_KEY}'
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching data from OMDB API: {e}")
            return

        movie_data = response.json()

        # Check if the movie exists
        if movie_data.get("Response") == "False":
            print(f"Movie '{title}' not found!")
            return

        title = movie_data.get("Title", title)
        year = movie_data.get("Year", year)
        rating = movie_data.get("imdbRating", rating)
        poster = movie_data.get("Poster", poster)

        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }

        self._write_storage(movies)
        print(f"Movie '{title}' added successfully!")

    def delete_movie(self, title):
        movies = self.list_movies()
        lowercase_titles = {key.lower(): key for key in movies.keys()}

        if title.lower() in lowercase_titles:
            original_title = lowercase_titles[title.lower()]  # Get the original case title
            del movies[original_title]
            self._write_storage(movies)
            print(f"Movie '{original_title}' has been deleted.")
            return True
        else:
            print(f"Movie '{title}' is not in the database.")
            return False

    def update_movie(self, title, new_rating):
        movies = self.list_movies()
        lowercase_titles = {key.lower(): key for key in movies.keys()}

        if title.lower() in lowercase_titles:
            original_title = lowercase_titles[title.lower()]
            movies[original_title]["rating"] = new_rating
            self._write_storage(movies)  # Save the updated movies dictionary
            print(f"Movie '{original_title}' rating updated to {new_rating}")
            return True
        else:
            print(f"The movie '{title}' is not in the database.")
            return False
