import json
import aiohttp
import asyncio

"""
    This file is split into two parts.
    
    Part 1:
        calling the PokeAPI and save the response on all pokemons
    
    Part 2:
        filtering out the data we want to keep and store it in a json file
"""

# -------------------------------
#       PART 1
# -------------------------------

async def callApi(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            try:
                return await response.json()
            except aiohttp.ContentTypeError as e:
                print("Error decoding JSON:", e)
        else:
            print("Error:", response.status)
        return None

async def get_pokemon_data():
    pkm_data = {}
    async with aiohttp.ClientSession() as session:
        tasks = [callApi(session, f"https://pokeapi.co/api/v2/pokemon/{i}") for i in range(1, 152)]
        responses = await asyncio.gather(*tasks)
        for i, response in enumerate(responses):
            if response:
                pkm_data[i + 1] = response
    return pkm_data

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    pkm_data = loop.run_until_complete(get_pokemon_data())
    loop.close()


# -------------------------------
#       PART 2
# -------------------------------

# this is the dict were all the pokemons are stored
final_dict = {}

# loop through all first 151 pokemons
for i in range(1, 152):

    temp_data = pkm_data[i]

    # set dict for each pokemon, this way it clears for each loop
    pokemon_dict = {}

    # id
    pokemon_dict["id"] = temp_data["id"]

    # name
    pokemon_dict["name"] = temp_data["name"]

    # type
        # pokemon have 1 or 2 types, so we check and adapt
    if len(temp_data["types"]) > 1:
        types = []
        for i in temp_data["types"]:
            types.append(i["type"]["name"])
        pokemon_dict["type"] = types
    else:
        pokemon_dict["type"] = temp_data["types"][0]["type"]["name"]

    # stats
        # take all stats, including the total, and add as nested dict
    temp_dict = {
        "hp": temp_data["stats"][0]["base_stat"],
        "attack": temp_data["stats"][1]["base_stat"],
        "defense": temp_data["stats"][2]["base_stat"],
        "special-attack": temp_data["stats"][3]["base_stat"],
        "special-defense": temp_data["stats"][4]["base_stat"],
        "speed": temp_data["stats"][5]["base_stat"],
        "total": sum([
            temp_data["stats"][0]["base_stat"],
            temp_data["stats"][1]["base_stat"],
            temp_data["stats"][2]["base_stat"],
            temp_data["stats"][3]["base_stat"],
            temp_data["stats"][4]["base_stat"],
            temp_data["stats"][5]["base_stat"]
            ])
    }
    pokemon_dict["stats"] = temp_dict

    # take the current pokemon dict and add to the complete dict
    final_dict[pokemon_dict["id"]] = pokemon_dict


# save the pokemon data in a json file
with open("data/pokedex.json", "w") as json_file:
    json.dump(final_dict, json_file, indent=4)