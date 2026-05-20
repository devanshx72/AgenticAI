from pydantic import BaseModel, computed_field
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int
    weight: float # in kg
    height: float # in meters
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

patient_info = {
    "name": "John Doe",
    "age": 30,
    "weight": 70.5,
    "height": 1.75,
    "married": True,
    "allergies": ["penicillin", "shellfish"],
    "contact_details": {
        "email": "john.doe@example.com",
        "phone": "123-456-7890"
    }
}

patient1 = Patient(**patient_info)
print(f"Patient Name: {patient1.name}")
print(f"Patient Age: {patient1.age}")
print(f"Patient BMI: {patient1.bmi}")