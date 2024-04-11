from chroma.chroma import addTextToVectorDb
from lang_chain.strings import splittedTextInChunk


def addLongTextToVectorDb(text: str ):
    # divide the text into chunks
    splittedText = splittedTextInChunk(text)
    # for each chunk, embed it ad add it to the db
    addTextToVectorDb(splittedText)
    # return confirmation
    
    return "Text added to the DB"
