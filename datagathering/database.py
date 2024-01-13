import sqlite3
import json


# get pokemon data
with open("pokedex_gen1.json", "r") as file:
    pokemon = json.load(file)

# get evolution data
with open("evolutionChains.json", "r") as file:
    evolutionChain = json.load(file)



# Create SQLite database
conn = sqlite3.connect("../pokedex_MVC/project/pokemonDatabase.db")
cursor = conn.cursor()


# -------------------------------
# Table of Pokemon, Types and Evolution-chain
# -------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemon (
               id INTEGER PRIMARY KEY,
               name TEXT,
               hp INTEGER,
               attack INTEGER,
               defense INTEGER,
               specialAttack INTEGER,
               specialDefense INTEGER,
               speed INTEGER,
               totalStats INTEGER,
               evolutionChain INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemon_types (
        pokemon_id INTEGER,
        type TEXT,
        FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
    )
""")

for val in pokemon.values():
    # Inserting into the pokemon table
    cursor.execute("""
        INSERT INTO pokemon (
            id, name, hp,
            attack, defense, specialAttack,
            specialDefense, speed, totalStats, evolutionChain
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        val["id"], val["name"],
        val["stats"]["hp"], val["stats"]["attack"],
        val["stats"]["defense"], val["stats"]["special-attack"],
        val["stats"]["special-defense"], val["stats"]["speed"],
        val["stats"]["total"], val["evolution-chain"]
    ))
    
    # Extracting types and inserting into the pokemon_types table
    types = val["type"]
    if isinstance(types, str):  # If it's a single type
        types = [types]  # Convert to a list for uniform handling
    
    for t in types:
        cursor.execute("""
            INSERT INTO pokemon_types (
                       pokemon_id, type
                       )
            VALUES (?, ?)
        """, (val["id"], t))


    
# -------------------------------
# Table of Evolutions
# -------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS evolution (
               id INTEGER PRIMARY KEY,
               evolutionChain TEXT
    )
""")

for key, val in evolutionChain.items():
    cursor.execute("""
        INSERT INTO evolution (
                   id, evolutionChain
        )
        VALUES (?, ?)
""",
    [
        key, json.dumps(val)
    ]
)


# -------------------------------
# Table of Users
# -------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
               username TEXT PRIMARY KEY,
               email TEXT,
               password TEXT
    )
""")

cursor.execute("""
    INSERT INTO user (
               username, email, password
    )
    VALUES (?, ?, ?)
""",
    [
        "test", "test@gmail.com", "123abc"
    ]
)


# comming changes and close
conn.commit()
conn.close()