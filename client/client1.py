import requests
from fastapi import HTTPException

url = 'http://127.0.0.1:8000/predict'

user_input = "sfs fekfke kfskfsf jkfjekfe mkefeksfewfa nlfkelf"

response = requests.post(url, json={"data": user_input})

print(response.status_code)
print(response.json())

'''
Status Code:
- 200 : successfully executed
- 401 : invalid api key
- 422 : validation error
'''
