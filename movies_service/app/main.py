import os
import uvicorn
from fastapi import FastAPI, status, Query, HTTPException, Form, Header
import requests
import random
from keycloak import KeycloakOpenID

app = FastAPI()


KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

@app.post("/get_jwt_token")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def chech_for_role_test(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (chech_for_role_test(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.get("/get_random_movie")
async def get_random_movie(token: str = Header()):
    if (chech_for_role_test(token)):
        r_id = random.randint(298, 10000)
        r = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{r_id}", headers={'X-API-KEY': '700211e1-f970-499f-9957-6bca24e2adb1'})
        return r.json()
    else:
        return "Wrong JWT Token"

@app.get("/search_by_title")
async def search_by_title(title: str, token: str = Header()):
    if (chech_for_role_test(token)):
        r = requests.get(
            f"https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={title}",
            headers={'X-API-KEY': '700211e1-f970-499f-9957-6bca24e2adb1'}
        )
        return r.json()
    else:
        return "Wrong JWT Token"


@app.get("/get_movie_by_id")
async def get_movie_by_id(q: list | None = Query(), token: str = Header()):
    if (chech_for_role_test(token)):
        film_list = []
        for id in q:
            r = requests.get(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}",
                             headers={'X-API-KEY': '700211e1-f970-499f-9957-6bca24e2adb1'})
            film_list.append(r.json())
        return film_list
    else:
        return "Wrong JWT Token"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))