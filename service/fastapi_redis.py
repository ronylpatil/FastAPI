import json
import redis
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
# Initialize a Redis client connection to the Redis server running on localhost at port 6379, using database 0
rd = redis.Redis(host="localhost", port=6379, db=0)

@app.get("/")
def read_root() : 
    return "Hello World!"

@app.get("/name/{user_name}")
def greeting(user_name:str) :
    cache = rd.get(user_name)
    if cache :
        print('cache hit!') 
        return json.loads(cache)        # convert JSON to python obj
    else : 
        print('cache miss!')
        r = {"user": user_name.title(), "passkey" : random.randint(00000,99999)}
        rd.set(user_name, json.dumps(r))        # json.dumps - convert python obj into JSON string, making it suitable for redis db
        return JSONResponse(r)


# [it will look for changes in whole project directory, to limit this score use --reload-dir ./dir_name]
# server cmd: uvicorn service.fastapi_redis:app --reload --reload-dir ./service --host 127.0.0.1 --port 8000 
# install "httpie" to access API through "http :8000" cmd.
