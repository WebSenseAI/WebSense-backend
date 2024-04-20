import sqlite3
import uuid

def addNewBot(name: str, website: str, description: str, message: str, key: str):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('./db_config/config_database.db')

    # Create a cursor object
    c = conn.cursor()

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS bot_info
        (name text, website text, description text, message text, key text, id text)
    ''')
    
    #id = str(uuid.uuid4())
    id = 'luisbeqja_collection'
    

    # Insert a row of data
    c.execute("INSERT INTO bot_info VALUES (?, ?, ?, ?, ?, ?)",
              (name, website, description, message, key, id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    return 'Bot added successfully'