from pydantic import BaseModel
from typing import List, Dict


class Spec(BaseModel):
    crop: str
    location: str
    temperature: float
    stress: List[str]
    traits: List[str]
    scientific_basis: List[str]
    confidence: float