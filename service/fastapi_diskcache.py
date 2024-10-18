import json
import random
import pathlib
import diskcache as dc
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Create a disk cache instance
pathlib.Path("./cache").mkdir(parents=True, exist_ok=True)
cache = dc.Cache("./cache")  # Specify your cache directory


@app.get("/")
def read_root():
    return "Hello World!"


@app.get("/name/{user_name}")
def get_passkey(user_name: str):
    # if user_name present in cache, return it else return None
    cache_data = cache.get(user_name)
    if cache_data:
        print("cache hit!")
        return json.loads(cache_data)       # convert JSON type to python object
    else:
        print("cache miss!")
        r = {"user": user_name.title(), "passkey": random.randint(00000, 99999)}
        cache.set(user_name, json.dumps(r))     # json.dump: convert python obj to JSON string 
        return JSONResponse(r)  # convert python dictionary to json http response type


# [it will look for changes in whole project directory, to limit this score use --reload-dir ./dir_name]
# server cmd: uvicorn service.fastapi_redis:app --reload --reload-dir ./service --host 127.0.0.1 --port 8000 
# install "httpie" to access API through "http :8000" cmd.
