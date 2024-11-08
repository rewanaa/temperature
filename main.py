from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TemperatureOutput(BaseModel):
    temperature: float
    message: str

@app.get("/")
def welcome():
    return {"message": "Welcome to the Temperature Conversion API"}

@app.get("/convert_temperature")
def convert_temperature(
    temp: float = Query(..., description="Temperature value to convert"),
    from_unit: str = Query(..., regex="^(Celsius|Fahrenheit)$", description="Temperature unit to convert from (Celsius or Fahrenheit)"),
):
    if from_unit == "Celsius":
        converted_temp = (temp * 9 / 5) + 32
        message = f"{temp}°C is equal to {converted_temp}°F."
    elif from_unit == "Fahrenheit":
        converted_temp = (temp - 32) * 5 / 9
        message = f"{temp}°F is equal to {converted_temp}°C."
    else:
        message = "Invalid unit provided."
    
    return TemperatureOutput(temperature=converted_temp, message=message)
