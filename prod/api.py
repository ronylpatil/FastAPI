import os
import json
import redis
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# load password from secrets.yaml
# key = yaml.safe_load(open(f"{pathlib.Path(__name__).parent.parent.as_posix()}/secrets.yaml"))['redis_key']

redis_host = os.getenv("REDIS_HOST")  
redis_key = os.getenv("REDIS_KEY") 

app = FastAPI()
rd = redis.Redis(host=redis_host,
        port=6379,
        password=redis_key,
        ssl=True
    )

@app.get("/")
def read_root() : 
    return "Hello World!"

@app.get("/{user_name}")
def get_passkey(user_name:str) :
    cache = rd.get(user_name)
    if cache :
        print('cache hit!') 
        return json.loads(cache)        # convert JSON string to python dict because we're saving it into JSON string form
    else : 
        print('cache miss!')
        r = {"user": user_name.title(), "passkey" : random.randint(00000, 99999)}
        rd.set(user_name, json.dumps(r))        # json.dumps - python dict into JSON string, making it suitable for redis db
        return JSONResponse(r)


# [it will look for changes in whole project directory, to limit this score use --reload-dir ./dir_name]
# server cmd: uvicorn service.redis_upstash:app --reload --reload-dir ./service --host 127.0.0.1 --port 8000 
# install "httpie" to access API through "http :8000" cmd.
