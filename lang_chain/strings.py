from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np
from typing import List

def returnConentMap(n):
        return n.page_content

def splittedTextInChunk(textToEmbbed: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(textToEmbbed)    
    print(len(chunks))
    return chunks

def splittedMultipleTextsInChunk(textsToEmbbed: List[str]) -> List[str]:
    """
    Splits multiple texts into chunks

    Parameters
    ----------
    textsToEmbbed : list[str]
        The texts that will be splitted

    Returns
    -------
    list[str]
        The list of chunks
    """
    chunks = [splittedTextInChunk(t) for t in textsToEmbbed if t is not None]
    # flatten the list of lists
    chunks = [item for sublist in chunks for item in sublist]
    return chunks
