import json

def AddVectorToTable(table, vector, conn):
    # Add a vector to a table in the database.
    cursor = conn.cursor()
    # Prepare the data
    text = vector['text']
    vector_json = json.dumps(vector['vector'])
    
    cursor.execute(    
        f"INSERT INTO {table} (text, vector) VALUES (?, ?)",
        (text, vector_json)
    )
    conn.commit()
    conn.close()
    

def dot_product(vector1, vector2):
    return sum(i*j for i, j in zip(vector1, vector2))
    
    
def getAllDbVectors(table, conn):
    cursor = conn.cursor()

    cursor.execute(    
        f"SELECT text, vector FROM {table}"
    )
    
    # Fetch all vectors from the table
    vectors = cursor.fetchall()
    conn.close()
    return vectors


def GetSimilarVectors(table, vector, conn):
    cursor = conn.cursor()

    cursor.execute(    
        f"SELECT text, vector FROM {table}"
    )
    
    # Fetch all vectors from the table
    vectors = cursor.fetchall()

    # Calculate dot product with each vector
    scores = [(text, dot_product(vector['vector'], json.loads(vector_data))) for text, vector_data in vectors]

    # Sort by score
    scores.sort(key=lambda x: x[1], reverse=True)
    # Print top 5 similar vectors    
    conn.close()
    return scores[:5]