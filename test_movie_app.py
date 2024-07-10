import pytest
import os
from unittest.mock import patch
from movie_app import MovieApp
from storage_csv import StorageCsv


def test_list_movies_empty(tmp_path):
    """Test in case database is empty."""
    storage = StorageCsv(tmp_path / "movies.csv")
    movie_app = MovieApp(storage)
    with patch('builtins.print') as mocked_print:
        movie_app._command_list_movies()
        mocked_print.assert_called_with("No movies found in the database.")


def test_list_movies_non_empty(tmp_path):
    """Test listing movies when the database has movies."""
    storage = StorageCsv(tmp_path / "movies.csv")
    movie_app = MovieApp(storage)
    movie_app._storage.add_movie("Rocky", "1976", "8.1", "rocky.jpg")

    # Perform the command that lists movies and capture the output
    with patch('builtins.print') as mocked_print:
        movie_app._command_list_movies()
        output = mocked_print.call_args_list  # Capture all calls to print

        # Extract the printed lines for easier assertion
        printed_lines = [call[0][0] for call in output]  # Extract the first argument of each call

        # Assert that each expected line is found in the printed output
        assert "Title: Rocky" in printed_lines
        assert "Year: 1976" in printed_lines
        assert "Rating: 8.1" in printed_lines
        assert "Poster: https://m.media-amazon.com/images/M/MV5BNTBkMjg2MjYtYTZjOS00ODQ0LTg0MDEtM2FiNmJmOGU1NGEwXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX300.jpg" in printed_lines


def add_movie(self, title, year, rating, poster):
    """
    Adds a movie to the CSV storage.
    """
    movies = self.list_movies()
    if title in movies:
        print(f"Movie '{title}' already exists!")
        return

    # Assuming `poster` is a URL, extract the filename
    poster_filename = os.path.basename(poster)

    movies[title] = {
        "year": year,
        "rating": rating,
        "poster": poster_filename
    }

    self._write_storage(movies)
    print(f"Movie '{title}' added successfully!")


def test_delete_movie(tmp_path):
    """Test deleting an existing movie."""
    storage = StorageCsv(tmp_path / "movies.csv")
    movie_app = MovieApp(storage)
    movie_app._storage.add_movie("Rocky", "1976", "8.1", "rocky.jpg")
    with patch('builtins.input', side_effect=["Rocky"]):
        movie_app._command_delete_movie()
        movies = movie_app._storage.list_movies()
        assert "Rocky" not in movies


def test_update_movie(tmp_path):
    """Test updating the rating of an existing movie."""
    storage = StorageCsv(tmp_path / "movies.csv")
    movie_app = MovieApp(storage)
    movie_app._storage.add_movie("Rocky", "1976", "8.1", "rocky.jpg")
    with patch('builtins.input', side_effect=["Rocky", "9.0"]):
        movie_app._command_update_movie()
        movies = movie_app._storage.list_movies()
        assert movies["Rocky"]["rating"] == "9.0"


def test_generate_website(tmp_path):
    """Test the _generate_website function."""
    storage = StorageCsv(tmp_path / "movies.json")
    movie_app = MovieApp(storage)

    movie_app._storage.add_movie("Movie1", "2000", "7.5", "poster1.jpg")
    movie_app._storage.add_movie("Movie2", "2010", "8.2", "poster2.jpg")

    # Call  _generate_website
    movie_app._generate_website()

    # Check if the output file was generated successfully
    output_path = os.path.join(os.path.dirname(__file__), "index.html")  # Adjust path as per your project structure
    assert os.path.exists(output_path), "Website generation failed"


if __name__ == "__main__":
    pytest.main()
