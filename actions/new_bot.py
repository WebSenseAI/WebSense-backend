import sqlite3
import uuid

def addNewBot(name: str, website: str, description: str, message: str, key: str, user_id: str):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('./db_config/config_database.db')

    # Create a cursor object
    c = conn.cursor()

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS bot_info
        (name text, website text, description text, message text, key text, id text)
    ''')
    
    id = str(uuid.uuid4())
    

    # Insert a row of data
    c.execute("INSERT INTO bot_info VALUES (?, ?, ?, ?, ?, ?)",
              (name, website, description, message, key, id))
    
    print('Bot added successfully', user_id, id)
    # insert a id to users_info table in the column bot_id, now is empty string for user with this ID 'test_id'
    c.execute("UPDATE users_info SET bot_id = ? WHERE id = ?", (id, user_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    return 'Bot added successfully'