# pyright: reportAttributeAccessIssue=false

import requests 
from urllib.parse import urljoin
import json
import os
from dotenv import load_dotenv 
from geopy.geocoders import Nominatim



load_dotenv()
ORS_API_KEY = os.getenv("ORS_API_KEY")



def read_api_endpoint(endpoint="/taxi/", base_url="http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API-fel: {e}"}


def post_api_endpoint(endpoint="/predict", data={}, base_url="http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint)
    try:
        response = requests.post(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API-fel: {e}"}




def get_ors_driving_distance(pickup_location: str, dropoff_location: str) -> dict:
 
   
    geolocator = Nominatim(user_agent="taxi_price_predictor_ors", adapter_factory=None)

   
        start_loc = geolocator.geocode(pickup_location, timeout=5)  # type: ignore
        end_loc = geolocator.geocode(dropoff_location, timeout=5) # type: ignore

     
       
        start_lat, start_lon, _ = start_loc.point # type: ignore
        end_lat, end_lon, _ = end_loc.point # type: ignore

       
        coords = [
            [start_lon, start_lat],
            [end_lon, end_lat]
        ]

        headers = {
            'Accept': 'application/json',
            'Authorization': ORS_API_KEY
        }
        
        body = {
            "locations": coords,
            "metrics": ["duration", "distance"]
        }

    
        response = requests.post(
            'https://api.openrouteservice.org/v2/matrix/driving-car',
            json=body,
            headers=headers
        )
        response.raise_for_status()

        data = response.json()

        
        distance_meters = data['distances'][0][1]
        duration_seconds = data['durations'][0][1]

        return {
            "distance_km": distance_meters / 1000.0,
            "duration_minutes": duration_seconds / 60.0
        }

