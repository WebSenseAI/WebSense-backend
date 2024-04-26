from chroma.chroma import addTextToVectorDb
from lang_chain.strings import splittedTextInChunk, splittedMultipleTextsInChunk


def addLongTextToVectorDb(text: str, id: str):
    # divide the text into chunks
    splittedText = splittedTextInChunk(text)
    # for each chunk, embed it ad add it to the db
    addTextToVectorDb(splittedText, id)
    # return confirmation
    
    return "Text added to the DB"

def addMultipleLongTextToVectorDb(texts: list[str], id: str):
    # divide each text into chunks and then flatten
    splittedTexts = splittedMultipleTextsInChunk(texts)
    # for each chunk embed it and add it into db
    addTextToVectorDb(splittedTexts, id)