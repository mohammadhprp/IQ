from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.models.product import Product, AnalysisResponse
from app.gen.analyzer import ProductAnalyzer
from app.core.config import get_settings

router = APIRouter()

def get_analyzer() -> ProductAnalyzer:
    """Get a configured ProductAnalyzer instance."""
    settings = get_settings()
    try:
        return ProductAnalyzer(
            model_name=settings.LLM_MODEL_NAME,
            temperature=settings.LLM_TEMPERATURE
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize analyzer: {str(e)}"
        )

AnalyzerDependency = Annotated[ProductAnalyzer, Depends(get_analyzer)]

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_product(
    product: Product,
    analyzer: AnalyzerDependency
) -> AnalysisResponse:
    """
    Analyze a product and its comments.
    
    Args:
        product: The product to analyze
        analyzer: The product analyzer instance
        
    Returns:
        AnalysisResponse containing the analysis results
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        return analyzer.analyze_product(product)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
