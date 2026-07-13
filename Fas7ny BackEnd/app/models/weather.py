from pydantic import BaseModel

class Weather(BaseModel):
    temperature: float
    max_temp: float
    min_temp: float
    condition: str
    icon: str