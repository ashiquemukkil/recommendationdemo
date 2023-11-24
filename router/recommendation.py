""" Similar Products Recommendation file
"""
import concurrent.futures
from pymilvus import connections, Collection
from config import ALIAS, INVENTORY_NAME, USER, PASSWORD, HOST, PORT


class SimilarRecommendation:
    def __init__(self):
        """
        Initialize the Milvus connection with default parameters.
        """
        connections.connect(
            alias=ALIAS,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
        )

    def get_recommendation_updated_inventory(self, product_id: str):
        """
        Get product recommendations based on the given product ID.

        Args:
            product_id (str): The ID of the product.

        Returns:
            dict: A dictionary containing the result of the recommendation.
        """
        # Load the Milvus collection
        collection = Collection(INVENTORY_NAME)
        collection.load()

        # Query the collection for embeddings of the given product ID
        expression = f'variant_barcode == "{product_id}"'
        embeddings_result = collection.query(
            expr=expression,
            offset=0,
            limit=10,
            output_fields=["department", "combined_embeddings"],
            consistency_level="Strong",
        )

        if len(embeddings_result) > 0:
            # Search for similar products based on the embeddings
            similar_based_on_distance_results = collection.search(
                data=[embeddings_result[0]["combined_embeddings"]],
                anns_field="combined_embeddings",
                param={"metric_type": "L2", "params": {"nprobe": 10}},
                offset=0,
                limit=4,
                output_fields=["image_url", "description"],
                expr=f'department == "{embeddings_result[0]["department"]}"',
            )

            # Process and format the results
            updated_result = []
            for product in similar_based_on_distance_results[0]:
                para_dict = {}
                para_dict["variant_code"] = product.id
                para_dict["image_url"] = product.entity.get("image_url")
                para_dict["description"] = product.entity.get("description")
                updated_result.append(para_dict)

            # Query for random products in the same department
            expression = f'department == "{embeddings_result[0]["department"]}"'
            random_products = collection.query(
                expr=expression,
                offset=0,
                limit=7,
                output_fields=["image_url", "description"],
                consistency_level="Strong",
            )

            # Format and filter random product results
            random_products_results = [
                {
                    "variant_code": product["variant_barcode"],
                    "image_url": product["image_url"],
                    "description": product["description"],
                }
                for product in random_products
                if product["variant_barcode"]
                not in list(similar_based_on_distance_results[0].ids)
            ]

            # Combine and return the final results
            final_results = updated_result[1:] + random_products_results[:2]

            return {
                "similar_products": final_results,
                "msg": "SUCCESS",
            }
        else:
            return {
                "similar_products": [],
                "msg": "FAILED",
                "error_message": "Product id not found in the inventory.",
            }


# Function to process a list of product IDs concurrently
def process_product_ids(product_ids, complementary: False) -> dict:
    """
    Process a list of product IDs concurrently.

    Args:
        product_ids (list): List of product IDs to process.
        complementary (bool): Flag indicating whether to get complementary recommendations.

    Returns:
        dict: A dictionary containing the processed results for each product ID.
    """
    result_dict = {}

    num_threads = 4

    recommendation_class = SimilarRecommendation()

    # Initialize a multiprocessing pool with the number of processes
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit the 'process_product' function to the executor for each product ID
        # This will execute the function for each product ID concurrently
        if complementary:
            future_to_product = {
                executor.submit(
                    recommendation_class.goes_well_with_updated,
                    product_id,
                ): product_id
                for product_id in product_ids
            }
        else:
            future_to_product = {
                executor.submit(
                    recommendation_class.get_recommendation_updated_inventory,
                    product_id,
                ): product_id
                for product_id in product_ids
            }

        # Retrieve the results as they become available
        for future in concurrent.futures.as_completed(future_to_product):
            product_id = future_to_product[future]
            try:
                output = future.result()
                result_dict[product_id] = output
            except Exception as e:
                # Handle any exceptions raised during processing here
                print(f"Error processing product {product_id}: {e}")

    return result_dict
