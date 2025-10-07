import joblib
from fastapi import FastAPI
from pathlib import Path
from taxipred.backend.data_processing import TaxiData, PredictionInput, preprocess_input 


MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "gbr_final_model.joblib"


MODEL = joblib.load(MODEL_PATH) 
   

app = FastAPI()
taxi_data = TaxiData()

@app.get("/taxi/")
async def read_taxi_data():
    return taxi_data.to_json()

@app.post("/predict")
async def predict_price(input_data: PredictionInput):
    
    processed_df = preprocess_input(input_data)
        
    prediction = MODEL.predict(processed_df)[0]
        
    return {"predicted_price": round(float(prediction), 2)}
        
   