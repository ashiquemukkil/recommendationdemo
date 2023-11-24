""" API for recommendation
"""
from fastapi import APIRouter
import logging
from pydantic import BaseModel
from router.recommendation import SimilarRecommendation, process_product_ids

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/recommendation")


class ProductIdMultiple(BaseModel):
    """Model for receiving multiple product IDs"""

    product_id: list


class ProductId(BaseModel):
    """Model for receiving a single product ID"""

    product_id: str


@router.post("/similar-products")
def recommendation(Product: ProductId):
    """
    Get recommendations for a single product.

    Args:
        Product (ProductId): ProductId instance containing a single product ID.

    Returns:
        Recommendation: The recommendation for the product.
    """
    recommendation_class = SimilarRecommendation()
    recommendation = recommendation_class.get_recommendation_updated_inventory(
        product_id=Product.product_id
    )
    return recommendation


@router.post("/similar-multiple-products")
def recommendation_multiple(Product: ProductIdMultiple):
    """
    Get recommendations for multiple products.

    Args:
        Product (ProductIdMultiple): ProductIdMultiple instance containing a list of product IDs.

    Returns:
        Recommendation: The recommendations for the products.
    """
    recommendation = process_product_ids(Product.product_id, complementary=False)
    return recommendation
