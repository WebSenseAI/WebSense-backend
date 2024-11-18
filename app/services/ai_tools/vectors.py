from app.extensions import supabase
import uuid

from app.models.vector_model import VectorModel

DIMENSIONS = {
    'text-embedding-ada-002' : 1536,
    'gte-large' : 1024,
    'gte-small' : 384
}

def add_text_to_vector_db(vector_model: VectorModel, collection_id: str,access_token: str, model: str = 'text-embedding-ada-002') -> None:
    records = []
    for text,embed in vector_model.get_zip():
        records.append({
            "id" : str(uuid.uuid4()),
            "embedding" : list(embed),
            "content" : text
        })
    action = supabase.schema('scrap_collections').rpc('vector_insert_embeddings', {
        "params": {
            "collection_name": collection_id,
            "rows": records
        }
    })
    action.headers["Authorization"] = "Bearer " + access_token
    response = action.execute()
    return response
