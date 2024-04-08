import os
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from database.functions import (AddVectorToTable, GetSimilarVectors)
from database.connection import db

embeddings_model = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))

def returnConentMap(n):
        return n.page_content
    
def EmbbedLongText(textToEmbbed: str):
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    
    texts = text_splitter.create_documents([textToEmbbed])
    splittedText = list(map(returnConentMap, texts))

    embeddings = embeddings_model.embed_documents(splittedText)
    return {
        "splittedText": splittedText,
        "splittedTextEmbedded": embeddings        
    }

def EmbbedShortText(textToEmbbed: str):
    embedded_text = embeddings_model.embed_query(textToEmbbed)
    return {
        "text": textToEmbbed,
        "textEmbedded": embedded_text        
    }

def LoadEmbeddingsToDatabase(splittedTextEmbedded, splittedText):
    for i, emb in enumerate(splittedTextEmbedded):
        AddVectorToTable("vector", {
           "text": splittedText[i],
          "vector": emb
    }, db)
        
def GetSimilarVectorsFromDatabase(vector):  
    mostSimilarContext = GetSimilarVectors("vector", {
        "text": vector["text"],
        "vector": vector["textEmbedded"]
    }, db)
    similarContextSum = mostSimilarContext[0][0] + mostSimilarContext[1][0] + mostSimilarContext[2][0] + mostSimilarContext[3][0] + mostSimilarContext[4][0]
    return similarContextSum