import os
import statistics
import random


MENU = """
********** Movies Database **********
Menu:
0. Exit the Program
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Generate website
"""


class MovieApp:
    """Movie app class contains teh operations functions"""
    def __init__(self, storage):
        self._storage = storage  # instanciate

    def _command_list_movies(self):
        """List all the movies"""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found in the database.")
            return

        print("List of Movies:")
        print("-" * 40)
        for title, details in movies.items():
            print(f"Title: {title}")
            print(f"Year: {details.get('year', 'N/A')}")
            print(f"Rating: {details.get('rating', 'N/A')}")
            print(f"Poster: {details.get('poster', 'N/A')}")
            print("-" * 40)

    def _command_add_movie(self):
        """adds new movies"""
        title = input("Enter movie title: ")
        year = input("Enter movie year: ")
        rating = input("Enter movie rating: ")
        poster = input("Enter movie poster URL: ")
        self._storage.add_movie(title, year, rating, poster)

    def _command_delete_movie(self):
        """deletes a specific movie"""
        title = input("Enter the movie title to delete: ")
        self._storage.delete_movie(title)

    def _command_update_movie(self):
        """updates the movie rating only"""
        title = input("Enter the movie title to update: ")
        new_rating = input("Enter new rating: ")
        self._storage.update_movie(title, new_rating)

    def _command_movie_stats(self):
        """performs operations to find and display stats"""
        movies = self._storage.list_movies()
        total_movies = len(movies)
        print(f"Total movies: {total_movies}")

        ratings = []
        for details in movies.values():
            try:
                rating = float(details["rating"])  # Convert
                ratings.append(rating)
            except ValueError:
                print(f"Invalid rating: {details['rating']}. Skipping this entry.")

        if not ratings:
            print("No valid ratings found.")
            return

        print("Movies statistics - avg-med-high-low rating!!!")
        # Average
        avg_rating = sum(ratings) / total_movies
        print(f"The Average Rating is: {avg_rating}")

        # Median
        median_rating = statistics.median(ratings)
        print("The Median Rating:", median_rating)

        # Best Rating
        best_rating = max(ratings)
        print(f"The Best Rating: {best_rating}")

        # Worst rating
        worst_rating = min(ratings)
        print(f"The Worst Rating: {worst_rating}")

    def _command_random_movie(self):
        """Random movie generation function"""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found in the database.")
            return

        random_movie = random.choice(list(movies.items()))
        print(
            f"Random movie: {random_movie[0]} - Rating: {random_movie[1]['rating']} - Year: {random_movie[1]['year']}")

    def _command_search_movie(self):
        """Search movie function, input taken from the user"""
        search_input = input("Enter part of movie name: ")
        movies = self._storage.list_movies()

        search_results = [name for name in movies.keys() if search_input.lower() in name.lower()]

        if search_results:
            print("Result Matching")
            for result in search_results:
                print(result)
        else:
            print("No match was found for the entered movie!")

    def _command_movie_rating_sort(self):
        """Sort movies by rating, from highest to lowest."""
        try:
            movies = self._storage.list_movies()
            sorted_movies = sorted(movies.items(), key=lambda x: float(x[1]["rating"]), reverse=True)
            print("Here is the sorted list, best first, worst last!")
            for movie, details in sorted_movies:
                print(f"{movie} - Rating: {details['rating']} - Year: {details['year']}")
        except Exception as e:
            print(f"Error: {e}")

    def _generate_website(self):
        """Function to generate the website according to template (& create a file called index.html)"""
        TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "_static", "index_template.html")
        OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "index.html")

        movies = self._storage.list_movies()

        with open(TEMPLATE_PATH, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()

        app_title = "Fun Movies"
        template_content = template_content.replace("__TEMPLATE_TITLE__", app_title)

        # movie grid to display the year, poster, movie
        movie_grid = ""
        for movie, details in movies.items():
            movie_grid += f'<div class="movie-item">'
            movie_grid += f'<h3>{movie}</h3>'
            movie_grid += f'<p>Rating: {details["rating"]}</p>'
            movie_grid += f'<p>{details["year"]}</p>'
            if "poster" in details:  # check for the poster
                movie_grid += f'<p><img src="{details["poster"]}" alt="{movie}"></p>'
            else:
                movie_grid += '<p>Poster not available</p>'
            movie_grid += f'</div>\n'

        template_content = template_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

        with open(OUTPUT_PATH, "w", encoding="utf-8") as output_file:
            output_file.write(template_content)

        # notify the user the output file is generated
        print(f"Generated {OUTPUT_PATH} successfully!")

    def run(self):
        """The Run logic of the program, calling upon all related functions to perform certain actions listed on the
        menu"""
        while True:
            print(MENU)
            try:
                user_choice = int(input("Enter your choice (0-9): "))
                menu_options = {
                    0: _command_exit_program,
                    1: self._command_list_movies,
                    2: self._command_add_movie,
                    3: self._command_delete_movie,
                    4: self._command_update_movie,
                    5: self._command_movie_stats,
                    6: self._command_random_movie,
                    7: self._command_search_movie,
                    8: self._command_movie_rating_sort,
                    9: self._generate_website
                }
                if user_choice in menu_options:
                    menu_options[user_choice]()
                else:
                    print("Invalid Menu Option!!!")
            except ValueError:
                print("Please enter a valid number (between 0 - 9)")



def _command_exit_program():
    """EXIT function"""
    print("Bye!")
    quit()

