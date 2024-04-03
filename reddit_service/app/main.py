import os
import uvicorn
import requests
import httpx
from fastapi import FastAPI, Depends, HTTPException, status, Query
from typing import Annotated

from sqlalchemy.orm import Session

from database import favourites_database as database
from database.favourites_database import Favourites


app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/get_posts_for_subreddit")
async def get_posts_for_subreddit(subreddit: str, limit: int):
    async with httpx.AsyncClient() as client:
        url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
        headers = {'User-Agent': 'a simple script for my University project by /u/Bar0nGeddon'}
        try:
            response = await client.get(url, headers=headers)

            if response.status_code == 200:
                posts = response.json()['data']['children']
                results = {post['data']['title']: post['data']['url'] for post in posts}
                return results
            else:
                raise HTTPException(status_code=response.status_code, detail="Reddit API error")

        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail="Error while fetching data")


@app.get("/get_top_for_subreddit")
async def get_top_for_subreddit(subreddit: str, time_period: str, limit: int):
    try:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t={time_period}&limit={limit}"
        headers = {'User-Agent': 'MyRedditApp/0.1'}

        response = requests.get(url, headers=headers)
        posts = response.json()['data']['children']

        # Используем словарь для хранения результатов
        results = {post['data']['title']: post['data']['url'] for post in posts}

        if response.status_code == 200:
            return results

    except Exception as e:
        # Используем HTTPException для отправки сообщения об ошибке с соответствующим статус-кодом
        raise HTTPException(status_code=400, detail="Error while fetching data")

@app.get("/get_posts_for_user")
async def get_posts_for_user(username: str, limit: int):
    async with httpx.AsyncClient() as client:
        url = f"https://www.reddit.com/user/{username}/submitted.json?limit={limit}"
        headers = {'User-Agent': 'reddit-access-script by /u/yourusername'}
        try:
            response = await client.get(url, headers=headers)

            if response.status_code == 200:
                posts = response.json()['data']['children']
                results = {post['data']['title']: post['data']['url'] for post in posts}
                return results
            else:
                raise HTTPException(status_code=response.status_code, detail="Reddit API error")

        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail="Error while fetching data")

@app.get("/search_reddit")
async def search_reddit(query: str, subreddit: str = Query(None), limit: int = 10):
    async with httpx.AsyncClient() as client:
        base_url = "https://www.reddit.com"
        if subreddit:
            url = f"{base_url}/r/{subreddit}/search.json?q={query}&limit={limit}"
        else:
            url = f"{base_url}/search.json?q={query}&limit={limit}"

        headers = {'User-Agent': 'reddit-search-script by /u/yourusername'}
        try:
            response = await client.get(url, headers=headers)

            if response.status_code == 200:
                posts = response.json()['data']['children']
                results = {post['data']['title']: post['data']['url'] for post in posts}
                return results
            else:
                raise HTTPException(status_code=response.status_code, detail="Reddit API error")

        except httpx.RequestError as e:
            raise HTTPException(status_code=400, detail=f"Error while fetching data: {str(e)}")

@app.post("/add_favourite")
async def add_favourite(name: str, url: str, db: db_dependency):
    try:
        new_favourite = Favourites(name=name, url=url)
        db.add(new_favourite)
        db.commit()
        db.refresh(new_favourite)
        return new_favourite
    except Exception as e:
        raise HTTPException(status_code=404, detail="You are not logged in")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
