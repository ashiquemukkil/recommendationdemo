"""
Create embeddings for inventory data.
"""

import numpy as np
import pandas as pd
from PIL import Image
import concurrent.futures
from sentence_transformers import SentenceTransformer
from pymilvus import (
    connections,
    CollectionSchema,
    FieldSchema,
    DataType,
    Collection,
)
from tqdm import tqdm
from config import PROJECT_ROOT, ALIAS, USER, PASSWORD, HOST, PORT


# Establish a connection
connections.connect(
    alias=ALIAS,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
)

# Drop the collection if it already exists
# utility.drop_collection("Inventory_embeddings")


def create_collection():
    """
    Create a collection in Milvus to store inventory data.
    """
    print("Creating collections")
    variant_code = FieldSchema(
        name="variant_barcode", dtype=DataType.VARCHAR, max_length=200, is_primary=True
    )
    image_url = FieldSchema(name="image_url", dtype=DataType.VARCHAR, max_length=200)
    department = FieldSchema(name="department", dtype=DataType.VARCHAR, max_length=200)
    class_code = FieldSchema(name="class_code", dtype=DataType.VARCHAR, max_length=200)
    description = FieldSchema(
        name="description", dtype=DataType.VARCHAR, max_length=500
    )
    price = FieldSchema(name="price", dtype=DataType.DOUBLE, max_length=10)
    season = FieldSchema(name="season", dtype=DataType.VARCHAR, max_length=10)
    combined_embeddings = FieldSchema(
        name="combined_embeddings", dtype=DataType.FLOAT_VECTOR, dim=1024
    )
    # url = FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=500)
    schema = CollectionSchema(
        fields=[
            variant_code,
            image_url,
            department,
            class_code,
            description,
            price,
            season,
            combined_embeddings,
            # url,
        ],
        description="inventory...",
    )
    collection_name = "Inventory_embeddings"
    collection = Collection(
        name=collection_name, schema=schema, using="default", shards_num=2
    )
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 1000},
    }

    collection.create_index(field_name="combined_embeddings", index_params=index_params)
    collection.release()


try:
    collection = Collection("Inventory_embeddings")
    collection.load()
except Exception as error:
    create_collection()
    collection = Collection("Inventory_embeddings")
    collection.load()


def extract_combined_embeddings(
    model: object,
    inventory: pd.DataFrame,
):
    """
    Extract image and text embeddings for each product in an inventory dataframe and insert
    them into a Milvus collection.

    Args:
        model (object): SentenceTransformer model object to encode the text and images.
        inventory (pd.DataFrame): The inventory dataframe containing the products to be processed.

    Returns:
        None
    """
    try:
        inventory = inventory[1]
        # print(inventory)
        product_id = inventory["variant_code"]
        images_url = inventory["image_url"]
        product_text = inventory["description"]

        # Download and preprocess images
        imgs = Image.open(f"{PROJECT_ROOT}/images/{product_id}.jpg")
        # Encode image embeddings
        image_embeddings = model.encode(imgs)  # 512
        # Encode text embeddings
        text_embedding = model.encode(
            product_text, batch_size=1, convert_to_tensor=True
        ).numpy()  # 512
        # Combine image and text embeddings
        combined_emb = np.concatenate(
            (image_embeddings, text_embedding), axis=None
        ).tolist()#1024
        collection.insert(
            [
                [product_id],
                [images_url],
                [inventory["department_code"]],
                [inventory["class_code"]],
                [product_text],
                [inventory["price"]],
                [inventory["season"]],
                [combined_emb],
                # [inventory["url"]],
            ]
        )
    except Exception as error:
        print(product_id, error)


model = SentenceTransformer("clip-ViT-B-32")
data = pd.read_excel(f"{PROJECT_ROOT}/cleaned_data.xlsx")

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as procedure_extract:
    for output in tqdm(
        procedure_extract.map(
            extract_combined_embeddings,
            [model] * len(data),
            data.iterrows(),
        )
    ):
        del output
