from app.extensions import vx
from typing import List
import uuid

from app.models.vector_model import VectorModel

DIMENSIONS = {
    'text-embedding-ada-002' : 1536,
    'gte-large' : 1024,
    'gte-small' : 384
}

def add_text_to_vector_db(vector_model: VectorModel, collection_id: str, model: str = 'text-embedding-ada-002') -> None:
    collection = vx.get_or_create_collection(
        name=collection_id,
        dimension=DIMENSIONS.get(model, DIMENSIONS['text-embedding-ada-002'])
    )
    records = [
        (str(uuid.uuid4()),
         vector,
         {'content' : page})
         for page, vector in vector_model.get_zip()
    ]

    collection.upsert(records=records)
    collection.create_index()