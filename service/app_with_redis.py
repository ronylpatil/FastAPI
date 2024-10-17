import json
import redis
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
rd = redis.Redis(host="localhost", port=6379, db=0)

@app.get("/")
def read_root() : 
    return "Hello World!"

@app.get("/name/{user_name}")
def greeting(user_name:str) :
    cache = rd.get(user_name)
    if cache :
        print('cache hit!') 
        return json.loads(cache)        # convert JSON to python dict
    else : 
        print('cache miss!')
        r = {"user": user_name.title(), "passkey" : random.randint(00000,99999)}
        rd.set(user_name, json.dumps(r))        # json.dumps - convert JSON HTTP response type into JSON string, making it suitable for redis db
        return JSONResponse(r)

# if __name__ == "__main__" : 
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

# install "httpie" to access API through "http :8000" cmd.
