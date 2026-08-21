# Movie Recommendation System - Error Catalog

This project is **intentionally broken** for testing error detection and debugging.
Every intentional error is marked in the source with a comment:

```python
# INTENTIONAL ERROR #N: <error type> - <short description>
```

## Project Files

| File | Purpose | Errors |
|------|---------|--------|
| `movies.py` | Movie database and queries | #1, #3 |
| `app.py` | CLI application (main entry point) | #2 |
| `recommender.py` | Recommendation engine | #4, #5, #6, #7 |
| `tests/test_recommender.py` | Pytest test suite (16 tests) | #8 |

---

## Error Catalog

### Error #1 — KeyError (dataset / import blocker)
- **File:** `movies.py`, line 74
- **Code:** `VALID_GENRES = list(set(movie["genere"] for movie in MOVIES_DATABASE))`
- **Error:** `KeyError: 'genere'`
- **Why:** The movie dictionaries use the key `"genre"`, but this line looks up `"genere"` (typo). It runs at module level, so importing `movies` fails and blocks everything else.
- **Fix:** Change `"genere"` to `"genre"`.

### Error #2 — TypeError (main application)
- **File:** `app.py`, lines 52-55 (`add_rating`)
- **Code:** `rating = input("Enter your rating (0-10): ")` then `recommender.add_user_rating(movie_id, rating)`
- **Error:** `TypeError: '<' not supported between instances of 'str' and 'int'` (surfaces at `recommender.py` line 21)
- **Why:** `input()` always returns a string. `add_user_rating` compares it against integers (`rating < 0`). The `try/except` in `add_rating` only catches `ValueError`, so the app crashes.
- **Fix:** Convert before passing: `rating = float(input("Enter your rating (0-10): "))`.

### Error #3 — AttributeError
- **File:** `movies.py`, line 89 (`get_movies_by_genre`)
- **Code:** `return MOVIES_DATABASE.filter(lambda m: m["genre"] == genre)`
- **Error:** `AttributeError: 'list' object has no attribute 'filter'`
- **Why:** Python lists have no `.filter()` method (that is pandas/JS thinking).
- **Fix:** Use a list comprehension: `return [m for m in MOVIES_DATABASE if m["genre"] == genre]`.

### Error #4 — ModuleNotFoundError (import blocker)
- **File:** `recommender.py`, line 4
- **Code:** `from movies_nonexistent import MOVIES_DATABASE, get_movie_by_id, get_movies_by_genre`
- **Error:** `ModuleNotFoundError: No module named 'movies_nonexistent'`
- **Why:** The module is called `movies`, not `movies_nonexistent`.
- **Fix:** Change the import to `from movies import MOVIES_DATABASE, get_movie_by_id, get_movies_by_genre`.

### Error #5 — ValueError: math domain error (recommendation logic)
- **File:** `recommender.py`, line 35 (`calculate_similarity`)
- **Code:** `similarity = math.sqrt(genre_match - rating_diff)`
- **Error:** `ValueError: math domain error`
- **Why:** `genre_match` is 0 or 1; `rating_diff` can be up to ±9.3. When different genres have close ratings (e.g. 0 - 0.1), the value under `sqrt()` is negative.
- **Fix:** Clamp with abs: `math.sqrt(abs(genre_match - rating_diff))` (or redesign the formula).

### Error #6 — KeyError (recommendation scoring)
- **File:** `recommender.py`, line 73 (`_calculate_recommendation_score`)
- **Code:** `score += movie["score"]`
- **Error:** `KeyError: 'score'`
- **Why:** Movie dictionaries have a `"rating"` key, not `"score"`. Only visible after Errors #1/#4/#5 are fixed.
- **Fix:** Change `movie["score"]` to `movie["rating"]`.

### Error #7 — Logic error (recommendation ranking)
- **File:** `recommender.py`, line 56 (`get_recommendations`)
- **Code:** `recommendations.sort(key=lambda x: x[1])`
- **Error:** No exception — tests fail with `assert recommendations[i][1] >= recommendations[i + 1][1]` (results come back worst-first).
- **Why:** Sort is ascending; recommendations must be ranked highest-score first.
- **Fix:** Add `reverse=True`: `recommendations.sort(key=lambda x: x[1], reverse=True)`.

### Error #8 — NameError (in the test file)
- **File:** `tests/test_recommender.py`, line 51 (`test_drama_genre_available`)
- **Code:** `assert "Drama" in genre_list`
- **Error:** `NameError: name 'genre_list' is not defined. Did you mean: 'genres'?`
- **Why:** The local variable is named `genres`; the assertion references a typo'd name.
- **Fix:** Change `genre_list` to `genres`.

---

## Testing Flow (staged reveal)

The errors are layered: each fix reveals the next layer.

```
pytest tests/ -v
  1. Collection ERROR  -> KeyError: 'genere'            (Error #1)
  2. Fix #1 -> Collection ERROR -> ModuleNotFoundError   (Error #4)
  3. Fix #4 -> tests run:
        AttributeError ('filter')                        (Error #3)
        ValueError: math domain error  x4 tests          (Error #5)
        NameError: 'genre_list'                          (Error #8)
  4. Fix #5 -> KeyError: 'score'  x2 tests               (Error #6)
  5. Fix #6 -> ranking assertion failure                 (Error #7)
  6. Fix #7 -> only Error #8 remains
  7. Fix #8 -> 16/16 passed

python app.py  (after fixing #1 and #4)
  Menu option 4 -> enter ID 1, rating 8.5
  -> TypeError: '<' not supported ...                   (Error #2)
```

## Commands

```
python -m pytest tests/ -v      # run the test suite
python app.py                   # run the CLI application
```

## Expected Final State (all fixed)

All 16 tests pass:

```
tests/test_recommender.py::TestMoviesModule::test_movies_database_not_empty PASSED
tests/test_recommender.py::TestMoviesModule::test_get_movie_by_id_valid PASSED
tests/test_recommender.py::TestMoviesModule::test_get_movie_by_id_invalid PASSED
tests/test_recommender.py::TestMoviesModule::test_get_movies_by_genre PASSED
tests/test_recommender.py::TestMoviesModule::test_get_all_genres PASSED
tests/test_recommender.py::TestMoviesModule::test_drama_genre_available PASSED
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
============================== 16 passed ==============================
```
