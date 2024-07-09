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
        title_lower = title.lower()  # Convert title to lowercase for case insensitivity
        if title_lower in movies:
            movies[title_lower]["rating"] = new_rating
            self._save_movies(movies)  # Save the updated movies dictionary
            print(f"Movie '{title}' rating updated to {new_rating}")
            return True
        else:
            print(f"The movie '{title}' is not in the database.")
            return False

    def _save_movies(self, movies):
        with open(self.file_path, 'w', encoding="utf-8") as handle:
            json.dump(movies, handle, indent=4)