import requests

favourite_movie_url = 'http://localhost:8001'
get_movies_url = f'{favourite_movie_url}/get_movies'
get_movie_by_id_url = f'{favourite_movie_url}/get_movie_by_id'
add_movie_url = f'{favourite_movie_url}/add_movie'
delete_movie_url = f'{favourite_movie_url}/delete_movie'

movie_url = 'http://localhost:8000'
get_random_movie_url = f'{movie_url}/get_random_movie'
get_kinopoisk_movie_by_id_url = f'{movie_url}/get_movie_by_id'

new_movie = {
    "id": 0,
    "movie_name": "testName",
    "creation_date": "2024-02-29T14:42:44.260037",
    "genre": "testGenre",
    "director": "testDirector"
}

def test_1_add_favourite():
    res = requests.post(f"{add_movie_url}", json=new_movie)
    assert res.status_code == 200

def test_2_get_movies():
    res = requests.get(f"{get_movies_url}").json()
    assert new_movie in res


def test_3_get_get_movie_by_id():
    res = requests.get(f"{get_movie_by_id_url}?movie_id=0").json()
    assert res == new_movie


def test_4_delete_movie():
    res = requests.delete(f"{delete_movie_url}?movie_id=0").json()
    assert res == "Success"


def test_5_kinopoisk_by_id():
    res = requests.get(f"{get_kinopoisk_movie_by_id_url}?q=500").json()
    assert res[0]["nameRu"] == "Собачий полдень"

def test_6_get_random_movie():
    res = requests.get(f"{get_random_movie_url}?q=500")
    assert res.status_code == 200