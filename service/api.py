import pathlib
import joblib
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field


app = FastAPI()
api_keys = ['xgb0fws23']  # This is encrypted in the database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')  # use token authentication

def api_key_auth(api_key: str = Depends(oauth2_scheme)) :
     if api_key not in api_keys :
          raise HTTPException(
               status_code = status.HTTP_401_UNAUTHORIZED,
               detail = 'Invalid API key, please check the key'
          )

class WineqIp(BaseModel) : 
     fixed_acidity : float = Field(..., ge = 4.1, le = 16.4)
     volatile_acidity : float = Field(..., ge = 0.5, le = 1.98)
     citric_acid : float = Field(..., ge = 0, le = 1.5)
     residual_sugar : float = Field(..., ge = 0.5, le = 16)
     chlorides : float = Field(..., ge = 0.008, le = 0.7)
     free_sulfur_dioxide : float = Field(..., ge = 0.7, le = 70)
     total_sulfur_dioxide : float = Field(..., ge = 5, le = 290)
     density : float = Field(..., ge = 0.85, le = 1.5)
     pH : float = Field(..., ge = 2.6, le = 4.5)
     sulphates : float = Field(..., ge = 0.2, le = 2.5)
     alcohol : float = Field(..., ge = 8, le = 15)


def feat_gen(user_input: dict) -> dict : 
     user_input['total_acidity'] = user_input['fixed_acidity'] + user_input['volatile_acidity'] + user_input['citric_acid']

     user_input['acidity_to_pH_ratio'] = (lambda total_acidity, pH : 0 if pH == 0 else total_acidity / pH)(user_input['total_acidity'], user_input['pH'])

     user_input['free_sulfur_dioxide_to_total_sulfur_dioxide_ratio'] = (lambda free_sulfur_dioxide, total_sulfur_dioxide : 0 if total_sulfur_dioxide == 0 \
                                                                           else free_sulfur_dioxide / total_sulfur_dioxide)\
                                                                           (user_input['free_sulfur_dioxide'], user_input['total_sulfur_dioxide'])

     user_input['alcohol_to_acidity_ratio'] = (lambda alcohol, total_acidity : 0 if total_acidity == 0 else alcohol / total_acidity)\
                                                  (user_input['alcohol'], user_input['total_acidity'])

     user_input['residual_sugar_to_citric_acid_ratio'] = (lambda residual_sugar, citric_acid : 0 if citric_acid == 0 else residual_sugar / citric_acid)\
                                                            (user_input['residual_sugar'], user_input['citric_acid'])

     user_input['alcohol_to_density_ratio'] = (lambda alcohol, density : 0 if density == 0 else alcohol / density)(user_input['alcohol'], user_input['density'])
     user_input['total_alkalinity'] = user_input['pH'] + user_input['alcohol']
     user_input['total_minerals'] = user_input['chlorides'] + user_input['sulphates'] + user_input['residual_sugar']
     
     return user_input


# add dependencies = [Depends(api_key_auth)] after 'predict/'
@app.post('/predict', dependencies = [Depends(api_key_auth)])
async def predict_wineq(user_input : WineqIp) -> dict :
     processed_data = feat_gen(user_input.model_dump())

     input_data =   [[processed_data['fixed_acidity'], processed_data['volatile_acidity'], processed_data['citric_acid'], processed_data['residual_sugar'],
                    processed_data['chlorides'], processed_data['free_sulfur_dioxide'], processed_data['total_sulfur_dioxide'], processed_data['density'], 
                    processed_data['pH'], processed_data['sulphates'], processed_data['alcohol'], processed_data['total_acidity'], processed_data['acidity_to_pH_ratio'], 
                    processed_data['free_sulfur_dioxide_to_total_sulfur_dioxide_ratio'], processed_data['alcohol_to_acidity_ratio'], 
                    processed_data['residual_sugar_to_citric_acid_ratio'], processed_data['alcohol_to_density_ratio'], processed_data['total_alkalinity'], 
                    processed_data['total_minerals']]]

     curr_dir = pathlib.Path(__file__)
     home_dir = curr_dir.parent.parent
     path = f"{home_dir.as_posix()}/models/model.joblib"

     model = joblib.load(path)
     prediction = model.predict(input_data).tolist()
     pred_prob = model.predict_proba(input_data).tolist()

     predicted_class = prediction[0]
     confidence = float('{:.4f}'.format(pred_prob[0][prediction[0] - 3]))

     if confidence > 0.70 : return {'prediction' : {'predicted_class' : predicted_class, 'confidence' : confidence}} 
     else : return {'prediction': 'Unexpected result'}

if __name__ == '__main__' :
    import uvicorn
    uvicorn.run(app, host = '127.0.0.1', port = 8000)

# app_name: api (file name)
# port: 8000 (default)
# cmd: uvicorn service.api:app --reload