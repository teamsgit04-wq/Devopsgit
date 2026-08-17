"""Tests for the Movie Recommendation System."""

import pytest
import math
from movies import (
    MOVIES_DATABASE,
    get_movie_by_id,
    get_movies_by_genre,
    get_all_genres,
    get_top_rated_movies
)
from recommender import MovieRecommender


class TestMoviesModule:
    """Tests for the movies module."""

    def test_movies_database_not_empty(self):
        """Test that movies database is not empty."""
        assert len(MOVIES_DATABASE) > 0

    def test_get_movie_by_id_valid(self):
        """Test getting a movie by valid ID."""
        movie = get_movie_by_id(1)
        assert movie is not None
        assert movie["title"] == "The Shawshank Redemption"

    def test_get_movie_by_id_invalid(self):
        """Test getting a movie by invalid ID."""
        movie = get_movie_by_id(999)
        assert movie is None

    def test_get_movies_by_genre(self):
        """Test getting movies by genre."""
        # This test will fail due to AttributeError in get_movies_by_genre
        drama_movies = get_movies_by_genre("Drama")
        assert len(drama_movies) > 0
        for movie in drama_movies:
            assert movie["genre"] == "Drama"

    def test_get_all_genres(self):
        """Test getting all genres."""
        # This test will fail due to NameError in movies.py
        genres = get_all_genres()
        assert isinstance(genres, list)
        assert len(genres) > 0

    def test_get_top_rated_movies(self):
        """Test getting top rated movies."""
        # This test will fail due to IndexError in get_top_rated_movies
        top_movies = get_top_rated_movies(3)
        assert len(top_movies) == 3
        # Verify they are sorted by rating
        for i in range(len(top_movies) - 1):
            assert top_movies[i]["rating"] >= top_movies[i + 1]["rating"]


class TestMovieRecommender:
    """Tests for the MovieRecommender class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.recommender = MovieRecommender()

    def test_add_user_rating_valid(self):
        """Test adding a valid user rating."""
        # This test will fail due to TypeError (string passed instead of float)
        self.recommender.add_user_rating(1, 8.5)
        assert 1 in self.recommender.user_ratings
        assert self.recommender.user_ratings[1] == 8.5

    def test_add_user_rating_invalid(self):
        """Test adding an invalid user rating."""
        with pytest.raises(ValueError):
            self.recommender.add_user_rating(1, 15)  # Rating > 10

    def test_add_to_watch_history(self):
        """Test adding movie to watch history."""
        self.recommender.add_to_watch_history(1)
        assert 1 in self.recommender.watch_history

    def test_calculate_similarity(self):
        """Test similarity calculation between movies."""
        # This test will fail due to ValueError (math domain error)
        movie1 = get_movie_by_id(1)
        movie2 = get_movie_by_id(2)
        similarity = self.recommender.calculate_similarity(movie1, movie2)
        assert isinstance(similarity, float)
        assert not math.isnan(similarity)

    def test_get_recommendations(self):
        """Test getting recommendations."""
        # Add some ratings
        self.recommender.add_user_rating(1, 9.0)
        self.recommender.add_user_rating(2, 8.5)

        # This test will fail due to KeyError and logic errors
        recommendations = self.recommender.get_recommendations(3)
        assert len(recommendations) > 0
        assert len(recommendations) <= 3

        # Verify recommendations are sorted by score (highest first)
        for i in range(len(recommendations) - 1):
            assert recommendations[i][1] >= recommendations[i + 1][1]

    def test_get_similar_movies(self):
        """Test getting similar movies."""
        # This test will fail due to ValueError in calculate_similarity
        similar = self.recommender.get_similar_movies(1, 3)
        assert len(similar) > 0
        assert len(similar) <= 3
        for movie, score in similar:
            assert movie["id"] != 1  # Should not include the source movie

    def test_clear_history(self):
        """Test clearing user history."""
        self.recommender.add_user_rating(1, 9.0)
        self.recommender.add_to_watch_history(1)
        self.recommender.clear_history()
        assert len(self.recommender.user_ratings) == 0
        assert len(self.recommender.watch_history) == 0


class TestRecommendationLogic:
    """Tests for recommendation logic correctness."""

    def setup_method(self):
        """Set up test fixtures."""
        self.recommender = MovieRecommender()

    def test_recommendations_exclude_watched(self):
        """Test that recommendations exclude already watched movies."""
        # Add ratings and watch history
        self.recommender.add_user_rating(1, 9.0)
        self.recommender.add_to_watch_history(1)
        self.recommender.add_to_watch_history(2)

        # This test will fail due to KeyError in _calculate_recommendation_score
        recommendations = self.recommender.get_recommendations(5)
        watched_ids = [1, 2]
        for movie, score in recommendations:
            assert movie["id"] not in watched_ids

    def test_similarity_same_genre(self):
        """Test that movies of same genre have higher similarity."""
        # This test will fail due to ValueError in calculate_similarity
        sci_fi_movie1 = get_movie_by_id(5)  # Inception - Sci-Fi
        sci_fi_movie2 = get_movie_by_id(6)  # The Matrix - Sci-Fi
        drama_movie = get_movie_by_id(1)    # Shawshank - Drama

        sim_same_genre = self.recommender.calculate_similarity(sci_fi_movie1, sci_fi_movie2)
        sim_diff_genre = self.recommender.calculate_similarity(sci_fi_movie1, drama_movie)

        assert sim_same_genre > sim_diff_genre
