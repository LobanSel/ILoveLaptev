import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'movies_service/app'))
sys.path.append(str(BASE_DIR / 'favourite_service/app'))

from movies_service.app.main import service_alive as movies_status
from favourite_service.app.main import service_alive as favourite_status


@pytest.mark.asyncio
async def test_movies_service_connection():
    r = await movies_status()
    assert r == {'message': 'service alive'}

@pytest.mark.asyncio
async def test_favourite_service_connection():
    r = await favourite_status()
    assert r == {'message': 'service alive'}
