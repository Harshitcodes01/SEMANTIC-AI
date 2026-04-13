from pydantic import BaseModel, Field
from typing import List


class Spec(BaseModel):
    crop: str = Field(min_length=1)
    location: str = Field(min_length=1)
    temperature: float
    stress: List[str]
    traits: List[str]
    scientific_basis: List[str]
    confidence: float = Field(ge=0.0, le=1.0)