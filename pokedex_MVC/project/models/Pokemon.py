import sqlite3
import ast
from project.weakness_calculator import find_weakness

#this methods finds the pokemon and all related data
def find_pokemon(name):
    conn = sqlite3.connect("project/pokemonDatabase.db")
    cursor = conn.cursor()

    # find pokemon data
    def find_pkm(name):
        query2 = "SELECT * FROM pokemon WHERE name = ?"
        cursor.execute(query2, (name,))
        pkm = cursor.fetchall()
        pkm = pkm[0]
        return pkm

    # find types of pokemon
    def find_types(name):
        query1 = ("""
            SELECT p.name AS pokemon_name, pt.type AS pokemon_type
            FROM pokemon p
            JOIN pokemon_types pt ON p.id = pt.pokemon_id
            WHERE p.name = ?
        """)
        cursor.execute(query1, (name,))
        types = cursor.fetchall()

        pokemon_types = {}
        for t in types:
            key = t[0]
            if key not in pokemon_types:
                pokemon_types[key] = []
            pokemon_types[key].append(t[1:])
        types = pokemon_types.get(name, [])
        
        # Convert tuples to strings and format them
        types_as_strings = [t[0] for t in types]
        return types_as_strings

    # find evolutions to pokemon
    def find_evo(evo_id):
        query3 = ("""
            SELECT evolutionChain
            FROM evolution
            WHERE id = ?
        """)
        cursor.execute(query3, (evo_id,))
        evolution = cursor.fetchall()
        evolution = evolution[0][0]
        evolution = ast.literal_eval(evolution)

        new_evolution = []
        for evo in evolution:
            temp_pkm = find_pkm(evo)
            new_evolution.append(temp_pkm)
        return new_evolution

    # create correct image url for pkm
    def create_img(pkm_id):
        if len(str(pkm_id)) == 1:
            img_link = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/00{str(pkm_id)}.png"
        elif len(str(pkm_id)) == 2:
            img_link = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/0{str(pkm_id)}.png"
        else:
            img_link = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{str(pkm_id)}.png"
        return img_link
    

    pkm = find_pkm(name)    # base pkm data
    types = find_types(name)    # types of pkm
    evolutions = find_evo(pkm[9])   # evolutions of pkm
    img_url = create_img(pkm[0])

    # get all data on all evolutions
    evolution_list = []
    for evo in evolutions:
        temp_type = find_types(evo[1])
        temp_img = create_img(evo[0])
        evolution_list.append([evo[0], evo[1], temp_type, evo[2], evo[3], evo[4], evo[5], evo[6], evo[7], evo[8], temp_img])
    conn.close()

    # find the damage taken from all types
    pkm_weakness = find_weakness(types)
    
    # make new list with all the data from pokemons
    new_pokemon = [pkm[0], pkm[1], types, pkm[2], pkm[3], pkm[4], pkm[5], pkm[6], pkm[7], pkm[8], img_url, evolution_list, pkm_weakness]
    
    return new_pokemon



# checking all the damage mulitplyers for the pokemon type
def check_damage(pkm):
    has_4x_damage = any(val == 4.0 for val in pkm[12].values())
    has_2x_damage = any(val == 2.0 for val in pkm[12].values())
    has_1x_damage = any(val == 1 for val in pkm[12].values())
    has_05x_damage = any(val == 0.5 for val in pkm[12].values())
    has_025x_damage = any(val == 0.25 for val in pkm[12].values())
    has_0x_damage = any(val == 0 for val in pkm[12].values())

    return has_4x_damage, has_2x_damage, has_1x_damage, has_05x_damage, has_025x_damage, has_0x_damage