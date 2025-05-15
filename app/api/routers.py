from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv

from app.models.product import Product, AnalysisResponse
from app.gen.analyzer import ProductAnalyzer
import os


load_dotenv() 
router = APIRouter()

def get_analyzer():
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not configured")
    return ProductAnalyzer(google_api_key=google_api_key)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_product(
    product: Product,
    analyzer: ProductAnalyzer = Depends(get_analyzer)
):
    try:
        return analyzer.analyze_product(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
