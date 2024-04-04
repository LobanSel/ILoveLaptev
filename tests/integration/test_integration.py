import asyncpg
import requests


async def test_database_connection():
    try:
        connection = await asyncpg.connect("postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query")
        assert connection.is_connected()
        await connection.close()
    except Exception as e:
        assert False, f"Не удалось подключиться к базе данных: {e}"

async def test_kinopoisk_api():
    headers = {"X-API-KEY": "700211e1-f970-499f-9957-6bca24e2adb1"}
    r = requests.get("https://kinopoiskapiunofficial.tech/api/v2.2/films/500", headers=headers)
    assert r.status_code == 200

async def test_movies_service_connection():
    r = requests.get("http://localhost:8000/health")
    assert r == {'message': 'service alive'}

async def test_favourite_service_connection():
    r = requests.get("http://localhost:8001/health")
    assert r == {'message': 'service alive'}
