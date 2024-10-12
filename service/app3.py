import logging
import asyncio
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import diskcache as dc
import hashlib

app = FastAPI()

# CORS Middleware to allow FastAPI to filter and control incoming requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a disk cache instance
cache = dc.Cache('./cache')  # Specify your cache directory

# Define a Pydantic model for the prediction request
class PredictionRequest(BaseModel):
    data: str

# Function to get cached prediction from disk cache
async def get_cached_prediction(data: str) -> int:
    # Use the hash of the input data as the cache key
    cache_key = hashlib.md5(data.encode()).hexdigest()
    
    # Check if the prediction exists in disk cache
    cached_result = cache.get(cache_key)
    
    if cached_result is not None:
        logger.info(f"Cache hit for input: {data}")
        return cached_result  # Return cached result
    
    logger.info(f"Cache miss for input: {data}, computing prediction...")
    
    # If cache miss, compute the prediction
    prediction = await predict(data)
    
    # Store the prediction in disk cache
    cache.set(cache_key, prediction)  # No expiration; you can add `expire` if needed
    
    return prediction

# Simulate the prediction logic
async def predict(data: str) -> int:
    # Simulate IO-bound operation (this could be where an actual model prediction happens)
    await asyncio.sleep(1)
    
    # For example, if there are more than 20 words in the data, return 1
    if len(data.split(' ')) > 20:
        return 1
    else:
        return 0

# Define the prediction endpoint
@app.post("/predict", response_model=PredictionRequest)
async def predict_endpoint(request: PredictionRequest):
    try:
        # Get the cached prediction or compute it if not in cache
        prediction = await get_cached_prediction(request.data)
        logger.info(f"Prediction made: {prediction}")
        return JSONResponse(content={"prediction": prediction})
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# app_name: api3 (file name)
# port: 8000 (default)
# cmd: uvicorn service.app3:app --reload
    