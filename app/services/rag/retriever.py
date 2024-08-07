import openai
from app.extensions import vx

DIMENSIONS = {
    'text-embedding-ada-002' : 1536,
    'gte-large' : 1024,
    'gte-small' : 384
}

def retriever(collection_id: str, qustion: str, model: str = 'text-embedding-ada-002'):
    
    collection = vx.get_or_create_collection(
        name=collection_id,
        dimension=DIMENSIONS.get(model, DIMENSIONS['text-embedding-ada-002'])
    )
    query_embedding = openai.embeddings.create(
        input=qustion,
        model=model
    )
    
    embedding_result = query_embedding.data[0].embedding
        
    try:
        results = collection.query(
            data=embedding_result,
            limit=5,
            include_metadata=True
        )
        return results[0][1]['content']
    except Exception as e:
        print('Error',e)
        return 'Error'
    