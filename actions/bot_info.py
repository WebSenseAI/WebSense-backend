import sqlite3


def getBotById(bot_id: str):
    # Connect to the SQLite database
    conn = sqlite3.connect('./db_config/config_database.db')
    # Create a cursor object
    c = conn.cursor()
    # Execute the query
    c.execute("SELECT * FROM bot_info WHERE id=?", (bot_id,))
    # Fetch the result
    bot = c.fetchone()
    # Close the connection
    conn.close()
    # Return the result
    # transform bot in json 
    return {
        'name': bot[0],
        'website': bot[1],
        'description': bot[2],
        'message': bot[3],
        'key': bot[4],
        'id': bot[5]
    }