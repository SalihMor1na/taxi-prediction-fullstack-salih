from pydantic import BaseModel 
import pandas as pd
import numpy as np 
from pathlib import Path 


class PredictionInput(BaseModel):
    Trip_Distance_km: float
    Time_of_Day: str 
    Day_of_Week: str  
    Passenger_Count: int
    Traffic_Conditions: str 
    Weather: str        
    Base_Fare: float
    Per_Km_Rate: float
    Per_Minute_Rate: float
    Trip_Duration_Minutes: float


EXPECTED_COLUMNS = [
    'Trip_Distance_km', 
    'Passenger_Count', 
    'Base_Fare', 
    'Per_Km_Rate', 
    'Per_Minute_Rate', 
    'Trip_Duration_Minutes',
    'Time_of_Day_Evening', 'Time_of_Day_Morning', 'Time_of_Day_Night', 
    'Day_of_Week_Weekend',
    'Traffic_Conditions_Low', 'Traffic_Conditions_Medium', 
    'Weather_Rain', 'Weather_Snow',
]


def preprocess_input(data: PredictionInput) -> pd.DataFrame:
    
    input_df = pd.DataFrame([data.model_dump()])

    categorical_features = ['Time_of_Day', 'Day_of_Week', 'Traffic_Conditions', 'Weather']
    input_df = pd.get_dummies(input_df, columns=categorical_features) 

    input_df = input_df.reindex(columns=EXPECTED_COLUMNS, fill_value=0)

    return input_df.astype(np.float32) 


class TaxiData:
    def __init__(self):
        CLEANED_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "cleaned_train_data.csv"
        
        self.df = pd.read_csv(CLEANED_DATA_PATH)
      
        self.df = pd.DataFrame() 
            

    def to_json(self):
        return self.df.to_dict(orient="records")


if __name__ == "__main__":
    taxi_data = TaxiData()
    print(taxi_data.to_json())
