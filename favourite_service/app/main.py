import os
import uvicorn
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

@app.get("/get_all_favourites")
async def get_all_favourites(db: db_dependency):
    favourites_list = db.query(Favourites).all()
    return {favourite.name: favourite.url for favourite in favourites_list}


@app.delete("/delete_favourite")
async def delete_favourite(favourite_name: str, db: db_dependency):
    favourite_item = db.query(Favourites).filter(Favourites.name == favourite_name).first()
    if not favourite_item:
        raise HTTPException(status_code=404, detail="Favourite not found")

    db.delete(favourite_item)
    db.commit()
    return {"detail": "Favourite deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
