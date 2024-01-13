import sqlite3

def pokemon_exist(name):
    conn = sqlite3.connect("project/pokemonDatabase.db")
    cursor = conn.cursor()

    query = "SELECT * FROM pokemon WHERE name = ?"
    
    try:
        cursor.execute(query, (name,))
        pkm = cursor.fetchall()
        pkm = pkm[0]
        return pkm
    except:
        return False