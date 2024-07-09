from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        try:
            with open(self.file_path, 'r') as handle:
                movies_data = json.load(handle)
            return movies_data
        except FileNotFoundError:
            return {}

    def add_movie(self, title, year, rating, poster):
        movies = self.list_movies()
        if title in movies:
            print(f"Movie '{title}' already exists!")
            return

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
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            print(f"Movie '{title}' has been deleted.")
            return True
        else:
            print(f"Movie '{title}' is not in the database.")
            return False

    def update_movie(self, title, rating):
        movies = self.list_movies()
        if title in movies:
            movies[title]["rating"] = rating
            self._save_movies(movies)
            print(f"Movie '{title}' rating updated to {rating}")
            return True
        else:
            print(f"The movie '{title}' is not in the database.")
            return False

    def _save_movies(self, movies):
        with open(self.file_path, 'w', encoding="utf-8") as handle:
            json.dump(movies, handle, indent=4)