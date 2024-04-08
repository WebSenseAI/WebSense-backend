from openai_api.setup import client

def embedding(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    print(response.data[0].embedding)
    return response.data[0].embedding