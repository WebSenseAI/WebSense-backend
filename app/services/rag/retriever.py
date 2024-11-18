import openai
from app.extensions import supabase
from app.services.logging_manager import get_logger

logger = get_logger(__name__)

DIMENSIONS = {
    'text-embedding-ada-002' : 1536,
    'gte-large' : 1024,
    'gte-small' : 384
}

def retriever(collection_id: str, qustion: str, model: str = 'text-embedding-ada-002'):
    
    query_embedding = openai.embeddings.create(
        input=qustion,
        model=model
    )
    
    embedding_result = query_embedding.data[0].embedding
    data = supabase.schema('scrap_collections').rpc('vector_match_documents', {
        "collection_id": collection_id,
        "query_embedding": list(embedding_result)
    })
    result = data.execute()
    return "No data" if not result.data else result.data[0]["content"]
    
