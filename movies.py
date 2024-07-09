import statistics
from random import choice
import matplotlib.pyplot as plt
import movie_storage
import os
from storage_json import StorageJson
import storage_json

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


def main():
    """Main function: contains the main menu operations of the program"""
    while True:
        print(MENU)
        try:
            user_choice = int(input("Enter your choice (0-9): "))

            menu_options = {
                0: exit_program,
                1: list_movies,
                2: add_movie_prompt,
                3: delete_movie_prompt,
                4: update_movie_prompt,
                5: get_movie_stats,
                6: random_movie_rating,
                7: search_movie,
                8: movie_rating_sort,
                9: display_website
            }
            if user_choice in menu_options:
                menu_options[user_choice]()
            else:
                print("Invalid Menu Option!!!")
        except ValueError:
            print("Please enter a valid number (between 0 - 9)")


def display_website():
    """Function to generate the website according to template (& create a file called index.html)"""
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "_static", "index_template.html")
    OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "index.html")
    STYLE_PATH = os.path.join(os.path.dirname(__file__), "_static", "style.css")

    movies = movie_storage.storage.list_movies()

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
        if "poster" in details:  # if to check if the poster exists
            movie_grid += f'<p><img src="{details["poster"]}" alt="{movie}"></p>'
        else:
            movie_grid += '<p>Poster not available</p>'
        movie_grid += f'</div>\n'

    template_content = template_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as output_file:
        output_file.write(template_content)

    # notify the user the output file is generated
    print(f"Generated {OUTPUT_PATH} successfully!")


def list_movies():
    """Function to list the movies out"""
    movies = movie_storage.storage.list_movies()
    for movie, details in movies.items():
        print(f"{movie} - Rating: {details['rating']} - Year: {details['year']}")


def total_movies():
    """Function to sum up and list the movies out"""
    movies = movie_storage.storage.list_movies()
    return len(movies)


def add_movie_prompt():
    """Ask the user for movie title and add it to the database
      call add_movie and save_movie from the new movie_storage structure file"""
    try:
        movie_title = input("Please enter a movie to be added to the movie list: ").strip()
        movie_storage.add_movie(movie_title)
        print("Updated List of Movies:")
        list_movies()  # Display updated list after adding a new movie
    except Exception as e:
        print(f"Error: {e}")


def delete_movie_prompt():
    """Ask the user for movie title and delete it from the database"""
    try:
        movie_title = input("Please enter a movie to be deleted from the movie list: ").strip().lower()
        movie_title_lower = movie_title.lower()
        if movie_storage.delete_movie(movie_title_lower):
            print(f"Movie '{movie_title}' has been deleted.")
            print("Updated List of Movies:")
            list_movies(movie_storage.storage.list_movies())
        else:
            print(f"Movie '{movie_title}' was not found.---")
    except Exception as e:
        print(f"Error: {e}")


def update_movie_prompt():
    """Ask the user for movie title and new rating to update"""
    try:
        movie_title = input("Enter the movie title to update: ").strip()
        new_rating = float(input("Enter the new rating (1-10): "))
        if new_rating < 1 or new_rating > 10:
            print("Rating should be between 1 and 10.")
            return

        # Call update_movie with original title (case-insensitive handled in storage_json.py)
        movie_storage.update_movie(movie_title, new_rating)

        print("Updated movie List:")
        list_movies()
    except ValueError:
        print("Invalid rating! Please enter a valid movie rating.")



def get_movie_stats():
    """Movie statistics function, gets avg, med, highest and lowest"""
    movies = movie_storage.storage.list_movies()
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
    avg_rating = sum(ratings) / total_movies()
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


def random_movie_rating():
    """Random movie generation function"""
    try:
        movies = movie_storage.storage.list_movies()  # get the movie from movie.storage
        if not movies:
            print("No movies found in the database.")
            return

        random_movie = choice(list(movies.items()))
        print(
            f"Random movie: {random_movie[0]} - Rating: {random_movie[1]['rating']} - Year: {random_movie[1]['year']}")
    except Exception as e:
        print(f"Error: {e}")


def search_movie():
    """Search movie function, input taken from the user"""
    try:
        search_input = input("Enter part of movie name: ")
        movies = movie_storage.storage.list_movies()

        search_results = []  # Initialize an empty list to store search results

        for name in movies.keys():
            if search_input.lower() in name.lower():
                search_results.append(name)

        if search_results:
            print("Result Matching")
            for result in search_results:
                print(result)
        else:
            print("No match was found for the entered movie!")
    except Exception as e:
        print(f"Error: {e}")


def movie_rating_sort():
    """Sort movies by rating, from highest to lowest."""
    try:
        movies = movie_storage.storage.list_movies()
        sorted_movies = sorted(movies.items(), key=lambda x: float(x[1]["rating"]), reverse=True)
        print("Here is the sorted list, best first, worst last!")
        for movie, details in sorted_movies:
            print(f"{movie} - Rating: {details['rating']} - Year: {details['year']}")
    except Exception as e:
        print(f"Error: {e}")


def exit_program():
    """EXIT function"""
    print("Bye!")
    quit()


if __name__ == "__main__":
    main()
