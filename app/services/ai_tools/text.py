from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken
from typing import List

MAX_TOKENS = {
    "text-embedding-ada-002" : 8192,
    "gte-large" : 512
}

CHUNK_OVERLAP = 200

def count_tokens(text:str) -> int:
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(text)
    return len(tokens)


def split_text(text: str, model: str = 'text-embedding-ada-002') -> List[str]:
    max_tokens = MAX_TOKENS.get(model, MAX_TOKENS['text-embedding-ada-002'])

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_tokens,
        chunk_overlap= 200,
        length_function=count_tokens,
        is_separator_regex=False
    )
    chunks = text_splitter.split_text(text)    
    return chunks


def split_multiple_texts(texts: List[str], model: str = 'text-embedding-ada-002') -> List[str]:
    chunks = [split_text(t,model) for t in texts if t is not None]
    # flatten the list of lists
    chunks = [item for sublist in chunks for item in sublist]
    return chunks


