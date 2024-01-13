import sqlite3

# finds all pokemons in database and filter the needed data
def all_pokemons():
    conn = sqlite3.connect("project/pokemonDatabase.db")
    cursor = conn.cursor()

    # join pokemon type with the right pokemon
    cursor.execute("""
        SELECT p.name AS pokemon_name, pt.type AS pokemon_type
        FROM pokemon p
        JOIN pokemon_types pt ON p.id = pt.pokemon_id
    """)
    all_types = cursor.fetchall()

    # find all pokemons
    cursor.execute("SELECT * FROM pokemon")
    pokemons = cursor.fetchall()
    conn.close()

    # make new list with just the data needed for pokedex-page
    # [id, name, [type1, type2], img-url1]

    pokemon_types = {}
    for t in all_types:
        key = t[0]
        if key not in pokemon_types:
            pokemon_types[key] = []
        pokemon_types[key].append(t[1:])

    new_pokemons = []
    for pkm in pokemons:
        pkm_type = pkm[1]
        types = pokemon_types.get(pkm_type, [])
        
        # Convert tuples to strings and format them
        types_as_strings = [t[0] for t in types]
        if len(str(pkm[0])) == 1:
            new_pokemons.append([pkm[0], pkm_type, types_as_strings, f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/00{str(pkm[0])}.png"])
        elif len(str(pkm[0])) == 2:
            new_pokemons.append([pkm[0], pkm_type, types_as_strings, f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/0{str(pkm[0])}.png"])
        else:
            new_pokemons.append([pkm[0], pkm_type, types_as_strings, f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{str(pkm[0])}.png"])
    
    return new_pokemons