from chroma.config import create_collection
import uuid

def addTextToVectorDb(textToEmbbed: str, id: str):
    create_collection(id).add(
        documents = textToEmbbed,
        ids=[str(uuid.uuid4()) for _ in range(len(textToEmbbed))],
    )
    return "done"
    

def getSimilarVector(question: str, id: str):
    results = create_collection(id).query(
        query_texts=[question],
        n_results=4
    )
    return results["documents"]