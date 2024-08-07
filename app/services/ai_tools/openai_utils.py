import openai
from flask import current_app
import os
import numpy as np

openai.api_key = os.environ.get('OPENAI_API_KEY')

def get_embedding(texts: list[str], model="text-embedding-ada-002"):
    responses = openai.embeddings.create(
        input=texts,
        model=model
    )
    return [np.array(response.embedding) for response in responses.data]
    