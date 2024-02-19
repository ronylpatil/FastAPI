import requests
from fastapi import HTTPException

url = 'http://127.0.0.1:8000/predict'

# The client should pass the API key in the headers (for main api)
headers = { 
    'Content-Type': 'application/json',
    'Authorization': 'Bearer xgb0fws23'
}

user_input = {  
                'fixed_acidity': 8.784,
                'volatile_acidity': 0.580,
                'citric_acid': 0.318,
                'residual_sugar': 2.805,
                'chlorides': 0.066,
                'free_sulfur_dioxide': 10.0,
                'total_sulfur_dioxide': 27.0,
                'density': 0.9964,
                'pH': 3.32,
                'sulphates': 0.67,
                'alcohol': '11.273'     # 9.8
            }

response = requests.post(url, json = user_input, headers = headers)

print(response.status_code)
print(response.json())

'''
Status Code:
- 200 : successfully executed
- 401 : invalid api key
- 422 : validation error
'''
