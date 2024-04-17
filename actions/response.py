from chroma.chroma import getSimilarVector
from lang_chain.lang_chain import LangChainResponse

def getResponseFromAi(question: str, id: str):
    return LangChainResponse(question, id)