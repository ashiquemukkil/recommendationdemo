""" API for recommendation
"""
# import subprocess
from fastapi import APIRouter
import logging
from pydantic import BaseModel
from router.recommendation import SimilarRecommendation, process_product_ids
import pandas as pd


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/recommendation")

# from data_creation.create_embeddings import start_embedding

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

@router.get("/items/")
def get_items(index:int =0,unique:int=0):
    if unique:
        return pd.read_excel(f"cleaned_data.xlsx").iloc[index-1]['images']
    return pd.read_excel(f"cleaned_data.xlsx").loc[index*20:(index+1)*20,['images','variant_code']].values.tolist()


# @router.get("/create_embedd")
# def start_embed():
#     start_embedding()
#     # subprocess.run(['python3', 'data_creation/create_embeddings.py'], check=True)
#     return "STARTED //it will take more than 10min"

# @router.get("/get_embedding_status")
# def embedding_status():
#     file_path= 'status.txt'
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#         if lines:
#             return lines[-1].strip()
#     return "Unable to show"