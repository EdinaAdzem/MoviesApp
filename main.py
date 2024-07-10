from movie_app import MovieApp
from storage_csv import StorageCsv
from storage_json import StorageJson


def main():
    print("\033[91m🌟Welcome to the Movie App!🌟\033[0m")
    print("Choose your storage type:")
    print("1. JSON")
    print("2. CSV")

    choice = input("Enter your prefered storage type choice (1/2): ").strip()

    if choice == '1':
        storage = StorageJson('movies.json')
    elif choice == '2':
        storage = StorageCsv('movies.csv')
    else:
        print("Only two options...Try Again!")
        return

    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()
