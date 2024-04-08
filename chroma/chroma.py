import chromadb
from chromadb.config import Settings
from openai_api.setup import client

#CHROMA DB 
chroma_client = chromadb.Client(
   Settings(persist_directory="db/")
)

collection = chroma_client.create_collection(name="my_collection")

student_info = """
Alexandra Thompson, a 19-year-old computer science sophomore with a 3.7 GPA,
is a member of the programming and chess clubs who enjoys pizza, swimming, and hiking
in her free time in hopes of working at a tech company after graduating from the University of Washington.
"""

club_info = """
The university chess club provides an outlet for students to come together and enjoy playing
the classic strategy game of chess. Members of all skill levels are welcome, from beginners learning
the rules to experienced tournament players. The club typically meets a few times per week to play casual games,
participate in tournaments, analyze famous chess matches, and improve members' skills.
"""

university_info = """
The University of Washington, founded in 1861 in Seattle, is a public research university
with over 45,000 students across three campuses in Seattle, Tacoma, and Bothell.
As the flagship institution of the six public universities in Washington state,
UW encompasses over 500 buildings and 20 million square feet of space,
including one of the largest library systems in the world."""

def embedding(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    return response.data[0].embedding


def croma_api():
    collection.add(
        embeddings=[embedding(student_info), embedding(club_info), embedding(university_info)],
        documents = [student_info, club_info, university_info],
        metadatas = [{"source": "student info"},{"source": "club info"},{'source':'university info'}],
        ids = ["id1", "id2", "id3"]
    )
    
def get_all_db_vectors():
    results = collection.query(
        query_texts=["What is the student name?"],
        n_results=2
    )
    return results