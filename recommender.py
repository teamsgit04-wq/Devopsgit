"""Movie Recommendation Engine module."""

# INTENTIONAL ERROR #6: ImportError - importing from non-existent module
from movies_nonexistent import MOVIES_DATABASE, get_movie_by_id, get_movies_by_genre

import math


class MovieRecommender:
    """A simple movie recommendation system."""

    def __init__(self):
        self.user_ratings = {}
        self.watch_history = []

    def add_user_rating(self, movie_id, rating):
        """Add a user rating for a movie."""
        # INTENTIONAL ERROR #2: TypeError - passing string "8.5" instead of float 8.5
        # The validation will compare string to number
        if rating < 0 or rating > 10:
            raise ValueError("Rating must be between 0 and 10")
        self.user_ratings[movie_id] = rating

    def add_to_watch_history(self, movie_id):
        """Add a movie to watch history."""
        self.watch_history.append(movie_id)

    def calculate_similarity(self, movie1, movie2):
        """Calculate similarity score between two movies based on genre and rating."""
        # INTENTIONAL ERROR #7: ValueError - math domain error from negative sqrt
        genre_match = 1 if movie1["genre"] == movie2["genre"] else 0
        rating_diff = movie1["rating"] - movie2["rating"]

        # This formula is wrong - can produce negative values under sqrt
        similarity = math.sqrt(genre_match - rating_diff)
        return similarity

    def get_recommendations(self, count=3):
        """Get movie recommendations based on user ratings and watch history."""
        if not self.user_ratings:
            return []

        # INTENTIONAL ERROR #8: Logic Error
        # Should calculate similarity scores but instead just returns random movies
        # The logic is inverted - returns least similar movies
        recommendations = []
        all_movies = MOVIES_DATABASE

        for movie in all_movies:
            if movie["id"] not in self.watch_history:
                score = self._calculate_recommendation_score(movie)
                recommendations.append((movie, score))

        # INTENTIONAL ERROR: Sorting in wrong order (ascending instead of descending)
        # This means worst recommendations come first
        recommendations.sort(key=lambda x: x[1])

        return recommendations[:count]

    def _calculate_recommendation_score(self, movie):
        """Calculate recommendation score for a movie."""
        score = 0

        # Compare against user's rated movies
        for rated_id, rating in self.user_ratings.items():
            rated_movie = get_movie_by_id(rated_id)
            if rated_movie:
                similarity = self.calculate_similarity(rated_movie, movie)
                score += similarity * rating

        # INTENTIONAL ERROR #4: KeyError - accessing non-existent key
        # The movie dict has "rating" not "score"
        score += movie["score"]

        return score

    def get_similar_movies(self, movie_id, count=3):
        """Get movies similar to a given movie."""
        target_movie = get_movie_by_id(movie_id)
        if not target_movie:
            return []

        similarities = []
        for movie in MOVIES_DATABASE:
            if movie["id"] != movie_id:
                sim = self.calculate_similarity(target_movie, movie)
                similarities.append((movie, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:count]

    def clear_history(self):
        """Clear user watch history and ratings."""
        self.user_ratings = {}
        self.watch_history = []
# Movie Recommendation System

movies = [
    "Leo",
    "Jailer",
    "Vikram",
    "Master"
]

def recommend_movie():
    movie_name = input("Enter movie name: ")

    # Intentional error for testing
    movie = movies_database[movie_name]

    print("Recommended Movie:", movie)

recommend_movie()