import logging
import asyncio
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware allow FastAPI to filter and control incomming requests from different origin (ex. frontend)
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

# Define a Pydantic model for the prediction request
class PredictionRequest(BaseModel):
    data: str

# Define the predict function
async def predict(data: str) -> int:
    # Your prediction logic here
    await asyncio.sleep(1)  # Simulate IO-bound operation
    # count #words 
    if len(data.split(' ')) > 20:
        return 1
    else:
        return 0

# Define the prediction endpoint
@app.post("/predict", response_model=PredictionRequest)
async def predict_endpoint(request: PredictionRequest):
    try:
        prediction = await predict(request.data)
        logger.info(f"Prediction made: {prediction}")
        return JSONResponse(content={"prediction": prediction})
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

    
# app_name: api (file name)
# port: 8000 (default)
# cmd: uvicorn service.api2:app --reload
