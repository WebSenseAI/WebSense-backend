from langchain_text_splitters import RecursiveCharacterTextSplitter

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
