from importlib.resources import files
from pathlib import Path

#DATA_PATH = Path(__file__).parents[1] / "data" / "taci_trip_pricing.csv"

TAXI_CSV_PATH = files("taxipred").joinpath("data/taxi_trip_pricing.csv")
