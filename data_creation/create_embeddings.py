"""
Create embeddings for inventory data.
"""

import numpy as np
import pandas as pd
from PIL import Image
import urllib.request
import io
import concurrent.futures
from sentence_transformers import SentenceTransformer
from pymilvus import (
    connections,
    CollectionSchema,
    FieldSchema,
    DataType,
    Collection,
    utility
)
from tqdm import tqdm

ALIAS = "default"
USER = "username"
PASSWORD = "password"
HOST = "127.0.0.1"
PORT = "19530"

INVENTORY_NAME = "Inventory_embeddings"


# Establish a connection
connections.connect(
    alias=ALIAS,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
)

# Drop the collection if it already exists
utility.drop_collection("Inventory_embeddings")



def create_collection():
    """
    Create a collection in Milvus to store inventory data.
    """
    print("Creating collections")
    variant_code = FieldSchema(
        name="variant_barcode", dtype=DataType.VARCHAR, max_length=200, is_primary=True
    )
    image_url = FieldSchema(name="image_url", dtype=DataType.VARCHAR, max_length=200)
    description = FieldSchema(
        name="description", dtype=DataType.VARCHAR, max_length=500
    )
    price = FieldSchema(name="price", dtype=DataType.DOUBLE, max_length=10)
    combined_embeddings = FieldSchema(
        name="combined_embeddings", dtype=DataType.FLOAT_VECTOR, dim=1024
    )
    # url = FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=500)
    schema = CollectionSchema(
        fields=[
            variant_code,
            image_url,
            description,
            price,
            combined_embeddings
        ],
        description="inventory...",
    )
    collection_name = INVENTORY_NAME
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
    collection = Collection(INVENTORY_NAME)
    collection.load()
except Exception as error:
    create_collection()
    collection = Collection(INVENTORY_NAME)
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
        product_id = str(inventory["variant_code"])
        images_url = inventory["images"]
        product_text = inventory["description"]

        product_text = " ".join(product_text.split(" ")[:30])
        # Download and preprocess images

        with urllib.request.urlopen(images_url) as my_url_res:
            my_img_data = my_url_res.read()
        imgs = Image.open(io.BytesIO(my_img_data))
        imgs = imgs.resize((1000, 1000))

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
                [product_text],
                [float(inventory["price"])],
                [combined_emb],
            ]
        )
        
    except Exception as error:
        print(product_id, error,images_url)


model = SentenceTransformer("clip-ViT-B-32")
data = pd.read_excel(f"cleaned_data.xlsx").head(500)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as procedure_extract:
    for output in tqdm(
        procedure_extract.map(
            extract_combined_embeddings,
            [model] * len(data),
            data.iterrows(),
        )
    ):
        del output
