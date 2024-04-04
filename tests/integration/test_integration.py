import requests 

async def test_movies_service_connection():
    r = requests.get("http://localhost:8000/health")
    assert r == {'message': 'service alive'}

async def test_favourite_service_connection():
    r = requests.get("http://localhost:8001/health")
    assert r == {'message': 'service alive'}
