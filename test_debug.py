import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_book():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/books/", json={"title": "Sample Book", "author": "Author", "genre": "Fiction", "year_published": 2021, "summary": "A sample book."})
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Book"