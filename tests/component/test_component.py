import requests

reddit_url = 'http://localhost:8000'
get_posts_for_subreddit_url = f'{reddit_url}/get_posts_for_subreddit'
get_top_for_subreddit_url = f'{reddit_url}/get_top_for_subreddit'
get_posts_for_user_url = f'{reddit_url}/get_posts_for_user'
search_reddit_url = f'{reddit_url}/search_reddit'

favourite_url = 'http://localhost:8001'
add_favourite_url = f'{favourite_url}/add_favourite'
get_all_favourites_url = f'{favourite_url}/get_all_favourites'
delete_favourite_url = f'{favourite_url}/delete_favourite'

new_favourite_name = "Tuesday Daily Thread: Advanced questions"
new_favourite_url = "https://www.reddit.com/r/Python/comments/1btk4m5/tuesday_daily_thread_advanced_questions/"

def test_1_get_posts_for_subreddit():
    res = requests.get(f"{get_posts_for_subreddit_url}?subreddit=python&limit=5")
    assert res.status_code == 200


def test_2_get_top_for_subreddit():
    res = requests.get(f"{get_top_for_subreddit_url}?subreddit=python&time_period=day&limit=5")
    assert res.status_code == 200


def test_3_get_posts_for_user():
    res = requests.get(f"{get_posts_for_user_url}?username=GeneDefiant6537&limit=1")
    assert res.status_code == 200


def test_4_search_reddit():
    res = requests.get(f"{search_reddit_url}?query=test&subreddit=python&limit=1")
    assert res.status_code == 200


def test_5_add_favourite():
    res = requests.post(f"{add_favourite_url}?name={new_favourite_name}&url={new_favourite_url}").json()
    assert res.status_code == 200


def test_6_get_all_favourites():
    res = requests.get(f"{get_all_favourites_url}")
    assert res.status_code == 200

def test_7_delete_favourite():
    res = requests.delete(f"{delete_favourite_url}?favourite_id=1")
    assert res.status_code == 200
