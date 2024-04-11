from chroma.config import collection
from langchain_text_splitters import CharacterTextSplitter
import uuid

def addTextToVectorDb(textToEmbbed: str):
    collection.add(
        documents = textToEmbbed,
        ids=[str(uuid.uuid4()) for _ in range(len(textToEmbbed))],
    )
    return "done"
    

def getSimilarVector(question: str):
    results = collection.query(
        query_texts=[question],
        n_results=4
    )
    return results["documents"]