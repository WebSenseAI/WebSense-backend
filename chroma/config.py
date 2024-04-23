import os
import chromadb
import chromadb.utils.embedding_functions as embedding_functions


def create_collection(name: str):
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.environ.get('OPENAI_API_KEY'),
                model_name="text-embedding-ada-002"
            )
    chroma_client = chromadb.PersistentClient(path="db_chroma")
    collection = chroma_client.get_or_create_collection(name=name, embedding_function=openai_ef)
    return collection
        
