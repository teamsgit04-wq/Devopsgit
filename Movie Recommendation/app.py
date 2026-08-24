"""Main application for the Movie Recommendation System."""

from recommender import MovieRecommender
from movies import (
    MOVIES_DATABASE,
    get_movie_by_id,
    get_movies_by_genre,
)


def display_menu():
    """Display the main menu."""
    print("\n=== Movie Recommendation System ===")
    print("1. View All Movies")
    print("2. Search Movies by Genre")
    print("3. Get Recommendations")
    print("4. Add Movie Rating")
    print("5. View Top Rated Movies")
    print("6. Exit")
    print("===================================")


def view_all_movies():
    """Display all movies."""
    print("\n--- All Movies ---")
    for movie in MOVIES_DATABASE:
        print(f"{movie['id']}. {movie['title']} ({movie['year']}) - {movie['genre']} - Rating: {movie['rating']}")


def search_by_genre():
    """Search movies by genre."""
    genres = get_all_genres()
    print(f"\nAvailable genres: {', '.join(genres)}")
    genre = input("Enter genre: ")

    movies = get_movies_by_genre(genre)
    if movies:
        print(f"\n--- {genre} Movies ---")
        for movie in movies:
            print(f"{movie['id']}. {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")
    else:
        print("No movies found for this genre.")


def add_rating(recommender):
    """Add a rating for a movie."""
    view_all_movies()
    try:
        movie_id = int(input("\nEnter movie ID: "))
        # INTENTIONAL ERROR #2: TypeError - passing string where int expected
        rating = input("Enter your rating (0-10): ")  # This returns a string
        recommender.add_user_rating(movie_id, rating)  # Should convert to float
        print("Rating added successfully!")
    except ValueError as e:
        print(f"Invalid input: {e}")


def view_top_rated():
    """View top rated movies."""
    print("\n--- Top Rated Movies ---")
    try:
        movies = get_top_rated_movies(5)
        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")
    except IndexError as e:
        print(f"Error retrieving movies: {e}")


def get_recommendations(recommender):
    """Get movie recommendations."""
    if not recommender.user_ratings:
        print("\nPlease add some ratings first!")
        return

    print("\n--- Recommended Movies ---")
    try:
        recommendations = recommender.get_recommendations(3)
        for i, (movie, score) in enumerate(recommendations, 1):
            print(f"{i}. {movie['title']} ({movie['year']}) - Score: {score:.2f}")
    except (KeyError, ValueError) as e:
        print(f"Error getting recommendations: {e}")


def main():
    """Main function to run the Movie Recommendation System."""
    recommender = MovieRecommender()

    print("Welcome to the Movie Recommendation System!")

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ")

        if choice == "1":
            view_all_movies()
        elif choice == "2":
            search_by_genre()
        elif choice == "3
            get_recommendations(recommender)
        elif choice == "4":
            add_rating(recommender)
        elif choice == "5":
            view_top_rated()
        elif choice == "6":
            print("Thank you for using Movie Recommendation System!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    
