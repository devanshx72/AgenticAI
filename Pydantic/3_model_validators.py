from pydantic import BaseModel, model_validator
from typing import List

class Patient(BaseModel):
    name: str
    age: int
    weight: float # in kg
    height: float # in meters
    married: bool
    allergies: List[str]

    @model_validator(mode='before')
    @classmethod
    def validate_patient(cls, values):
        if values.get('age') < 0:
            raise ValueError("Age cannot be negative")
        if values.get('weight') <= 0:
            raise ValueError("Weight must be greater than zero")
        if values.get('height') <= 0:
            raise ValueError("Height must be greater than zero")
        return values