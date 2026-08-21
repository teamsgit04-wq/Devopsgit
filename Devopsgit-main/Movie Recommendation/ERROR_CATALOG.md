# Movie Recommendation System - Error Catalog

This project is **intentionally broken** for testing GitHub Team Monitor error detection and AI auto-correction.

## Project Files

| File | Purpose | Errors |
|------|---------|--------|
| `movies.py` | Movie database and queries | 3 errors |
| `recommender.py` | Recommendation engine | 4 errors |
| `app.py` | CLI application | 1 error |
| `tests/test_recommender.py` | Pytest test suite (16 tests) | All fail |

---

## Error Catalog

### Error #1 — KeyError
- **File:** `movies.py`
- **Line:** 75
- **Code:** `movie["genere"]`
- **Error:** `KeyError: 'genere'`
- **Cause:** Typo — key `"genere"` does not exist, should be `"genre"`
- **Fix:** Change `"genere"` to `"genre"`

### Error #2 — TypeError
- **File:** `app.py`
- **Line:** 85
- **Code:** `recommender.add_user_rating(movie_id, rating)` where `rating` is from `input()`
- **Error:** `TypeError: '<' not supported between instances of 'str' and 'int'`
- **Cause:** `input()` returns a string, compared against integers in validation
- **Fix:** Convert `rating` to `float` before passing: `rating = float(input(...))`

### Error #3 — IndexError
- **File:** `movies.py`
- **Line:** 87
- **Code:** `return sorted_movies[:count + 2]`
- **Error:** `IndexError: list index out of range` (when accessed by index in tests)
- **Cause:** Off-by-two slicing returns more items than expected, tests index beyond bounds
- **Fix:** Change `count + 2` to `count`

### Error #4 — KeyError
- **File:** `recommender.py`
- **Line:** 64
- **Code:** `score += movie["score"]`
- **Error:** `KeyError: 'score'`
- **Cause:** Movie dict has key `"rating"` not `"score"`
- **Fix:** Change `movie["score"]` to `movie["rating"]`

### Error #5 — AttributeError
- **File:** `movies.py`
- **Line:** 79
- **Code:** `MOVIES_DATABASE.filter(lambda m: m["genre"] == genre)`
- **Error:** `AttributeError: 'list' object has no attribute 'filter'`
- **Cause:** Python lists do not have a `.filter()` method
- **Fix:** Use list comprehension: `[m for m in MOVIES_DATABASE if m["genre"] == genre]`

### Error #6 — ModuleNotFoundError
- **File:** `recommender.py`
- **Line:** 4
- **Code:** `from movies_nonexistent import MOVIES_DATABASE, get_movie_by_id, get_movies_by_genre`
- **Error:** `ModuleNotFoundError: No module named 'movies_nonexistent'`
- **Cause:** Module name is wrong — should be `movies`
- **Fix:** Change `movies_nonexistent` to `movies`

### Error #7 — ValueError
- **File:** `recommender.py`
- **Line:** 37
- **Code:** `similarity = math.sqrt(genre_match - rating_diff)`
- **Error:** `ValueError: math domain error`
- **Cause:** `rating_diff` can exceed `genre_match`, producing a negative number under `sqrt()`
- **Fix:** Use `abs()` or clamp: `math.sqrt(abs(genre_match - rating_diff))`

### Error #8 — Logic Error
- **File:** `recommender.py`
- **Line:** 56
- **Code:** `recommendations.sort(key=lambda x: x[1])`
- **Error:** No exception — silently returns worst movies first
- **Cause:** Sort is ascending (lowest score first), should be descending
- **Fix:** Add `reverse=True`: `recommendations.sort(key=lambda x: x[1], reverse=True)`

---

## Testing Flow

```
pytest tests/ -v
  → Collection fails (Error #1 blocks import)
  → Fix Error #1 → collection proceeds, tests start running
  → Each fix reveals the next error
  → Fix all 8 → 16/16 tests pass
```

## Expected Test Results (All Fixed)

```
tests/test_recommender.py::TestMoviesModule::test_movies_database_not_empty PASSED
tests/test_recommender.py::TestMoviesModule::test_get_movie_by_id_valid PASSED
tests/test_recommender.py::TestMoviesModule::test_get_movie_by_id_invalid PASSED
tests/test_recommender.py::TestMoviesModule::test_get_movies_by_genre PASSED
tests/test_recommender.py::TestMoviesModule::test_get_all_genres PASSED
tests/test_recommender.py::TestMoviesModule::test_get_top_rated_movies PASSED
tests/test_recommender.py::TestMovieRecommender::test_add_user_rating_valid PASSED
tests/test_recommender.py::TestMovieRecommender::test_add_user_rating_invalid PASSED
tests/test_recommender.py::TestMovieRecommender::test_add_to_watch_history PASSED
tests/test_recommender.py::TestMovieRecommender::test_calculate_similarity PASSED
tests/test_recommender.py::TestMovieRecommender::test_get_recommendations PASSED
tests/test_recommender.py::TestMovieRecommender::test_get_similar_movies PASSED
tests/test_recommender.py::TestMovieRecommender::test_clear_history PASSED
tests/test_recommender.py::TestRecommendationLogic::test_recommendations_exclude_watched PASSED
tests/test_recommender.py::TestRecommendationLogic::test_similarity_same_genre PASSED
============================== 15 passed in 0.05s ==============================
```
