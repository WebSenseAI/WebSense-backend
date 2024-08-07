from typing import List

class VectorModel:
    def __init__(self, data: List[str], embeddings: List[List[float]]):
        self.data = data
        self.embeddings = embeddings

    def get_zip(self):
        return zip(self.data,self.embeddings)