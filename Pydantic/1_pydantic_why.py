from pydantic import BaseModel, EmailStr, AnyUrl
from typing import List, Dict, Optional

class Patient(BaseModel):
    name: str
    email: EmailStr
    linked_url: AnyUrl
    age: int
    weight: float
    married: bool
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserting patient into database...")

def update_patient(patient: Patient):
    print(f"Updating patient...")
    print(patient.name)
    print(patient.age)
    print(patient.allergies)

patient_info = {
    "name": "John Doe",
    "age": 30,
    "weight": 70.5,
    "email": "john.doe@example.com",
    "married": True,
    "linked_url": "https://www.example.com/profile/johndoe",
    # "allergies": ["penicillin", "shellfish"],
    "contact_details": {
        "email": "john.doe@example.com",
        "phone": "123-456-7890"
    }
}

patient1 = Patient(**patient_info)

update_patient(patient1)