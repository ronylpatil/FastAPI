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
def read_root() : 
    return "Hello World!"

@app.get("/name/{user_name}")
def get_passkey(user_name:str) :
    cache_data = cache.get(user_name)
    if cache_data :
        print('cache hit!') 
        return json.loads(cache_data)        # convert JSON to python dict
    else : 
        print('cache miss!')
        r = {"user": user_name.title(), "passkey" : random.randint(00000, 99999)}
        cache.set(user_name, json.dumps(r))        # json.dumps - convert JSON HTTP response type into JSON string, making it suitable for redis db
        return JSONResponse(r)

if __name__ == "__main__" : 
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# install "httpie" to access API through "http :8000/name/..." cmd.
