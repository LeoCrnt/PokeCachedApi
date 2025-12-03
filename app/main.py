from fastapi import FastAPI
import redis
import requests
import json
import os

app = FastAPI()

redis_host = os.getenv("REDIS_HOST","localhost")

cache = redis.Redis(host=redis_host,port=6379,decode_responses=True)

@app.get("/pokemon/{name}")
async def fetch_pokemon(name: str):

    cached_data = cache.get(name)
    if cached_data:
        print(f"cached")
        return json.loads(cached_data)

    print(f"not cached")
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Pokemon not found"}

    data = response.json()

    await cache.set(name, json.dumps(data), ex=20)

    return data

