from typing import List
from pydantic import BaseModel


class Comment(BaseModel):
    id: str
    user_id: str
    text: str


class Product(BaseModel):
    id: str
    name: str
    description: str
    comments: List[Comment]


class AnalysisResponse(BaseModel):
    rating: float
    summary: str
    fake_comments: List[str]
    keywords: List[str]
    pros: List[str]
    cons: List[str]
