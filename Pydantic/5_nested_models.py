from pydantic import BaseModel, ValidationError
from typing import List, Optional

class Address(BaseModel):
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: str
    age: int
    address: Address

address = Address(city="New York", state="NY", zip_code="10001")
patient_info = {
    "name": "John Doe",
    "age": 30,
    "address": address
}

patient = Patient(**patient_info)
print(patient)