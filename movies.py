"""Movie database module for the Movie Recommendation System."""

# INTENTIONAL ERROR #1: NameError - Using undefined variable 'genere' instead of 'genre'
# This will cause a NameError when the module is imported

MOVIES_DATABASE = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genre": "Drama",
        "rating": 9.3,
        "director": "Frank Darabont"
    },
    {
        "id": 2,
        "title": "The Godfather",
        "year": 1972,
        "genre": "Crime",
        "rating": 9.2,
        "director": "Francis Ford Coppola"
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "year": 2008,
        "genre": "Action",
        "rating": 9.0,
        "director": "Christopher Nolan"
    },
    {
        "id": 4,
        "title": "Pulp Fiction",
        "year": 1994,
        "genre": "Crime",
        "rating": 8.9,
        "director": "Quentin Tarantino"
    },
    {
        "id": 5,
        "title": "Inception",
        "year": 2010,
        "genre": "Sci-Fi",
        "rating": 8.8,
        "director": "Christopher Nolan"
    },
    {
        "id": 6,
        "title": "The Matrix",
        "year": 1999,
        "genre": "Sci-Fi",
        "rating": 8.7,
        "director": "The Wachowskis"
    },
    {
        "id": 7,
        "title": "Forrest Gump",
        "year": 1994,
        "genre": "Drama",
        "rating": 8.8,
        "director": "Robert Zemeckis"
    },
    {
        "id": 8,
        "title": "Interstellar",
        "year": 2014,
        "genre": "Sci-Fi",
        "rating": 8.6,
        "director": "Christopher Nolan"
    }
]

# INTENTIONAL ERROR #1: NameError - 'genere' is undefined (should be 'genre')
# This line references an undefined variable
VALID_GENRES = list(set(movie["genere"] for movie in MOVIES_DATABASE))


def get_movie_by_id(movie_id):
    """Get a movie by its ID."""
    for movie in MOVIES_DATABASE:
        if movie["id"] == movie_id:
            return movie
    return None


def get_movies_by_genre(genre):
    """Get all movies of a specific genre."""
    # INTENTIONAL ERROR #5: AttributeError - list has no attribute 'filter'
    # Should use list comprehension or filter() function
    return MOVIES_DATABASE.filter(lambda m: m["genre"] == genre)


def get_all_genres():
    """Get list of all unique genres."""
    return VALID_GENRES


def get_top_rated_movies(count=5):
    """Get top rated movies."""
    sorted_movies = sorted(MOVIES_DATABASE, key=lambda x: x["rating"], reverse=True)
    # INTENTIONAL ERROR #3: IndexError - accessing index that doesn't exist
    # If count > len(sorted_movies), this will fail
    return sorted_movies[:count + 2]


def search_movies_by_director(director):
    """Search movies by director name."""
    results = []
    for movie in MOVIES_DATABASE:
        if movie["director"] == director:
            results.append(movie)
    return results
