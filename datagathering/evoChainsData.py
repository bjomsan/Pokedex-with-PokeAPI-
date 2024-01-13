import json
import aiohttp
import asyncio


async def make_async_request(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            try:
                return await response.json()
            except aiohttp.ContentTypeError as e:
                print("Error decoding JSON:", e)
        else:
            print("Error:", response.status)

async def fetch_all_evolutions():
    all_evolutions = {}
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 79):
            tasks.append(make_async_request(session, f"https://pokeapi.co/api/v2/evolution-chain/{i}"))
        results = await asyncio.gather(*tasks)
        for i, result in enumerate(results, start=1):
            all_evolutions[i] = result
    return all_evolutions

async def main():
    all_evolutions = await fetch_all_evolutions()
    return all_evolutions

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    all_evolutions = loop.run_until_complete(fetch_all_evolutions())
    loop.close()




# filtered dict of all relevant evolution chains
evolution_chain = {}

for i in range(1, 79):

    """
        The number of evolutions vary from 1 - 3.

        We use try/except avoid any errors when the evolution does not exist,
        and we later check if the program found any evolution before adding
        the evolution chain to the complete dict.  
    """

    try:
        first_evo = all_evolutions[i]["chain"]["species"]["name"]
    except:
        first_evo = ""
    try:
        second_evo = all_evolutions[i]["chain"]["evolves_to"][0]["species"]["name"]
    except:
        second_evo = ""
    try:
        third_evo = all_evolutions[i]["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
    except:
        third_evo = ""


    if third_evo:
        evolution_chain[str(i)] = [first_evo, second_evo, third_evo]
    elif second_evo:
        evolution_chain[str(i)] = [first_evo, second_evo]
    else:
        evolution_chain[str(i)] = first_evo



# load in the data created in getpokedexData.py
with open("data/pokedex.json", "r") as file:
    poke_data = json.load(file) 


"""
    Some evolutions came in later generations.
    These are evolutions are included in the evo_data,
    so we need to locate these and remove them.
"""
# list of all pokemons in poke_data
another_pkmlist = [poke_data[str(i)]["name"] for i in range(1, 152)]

# loop through all evolutions and remove those who are not in the orig 151 
for i in range(1, 79):
    temp = evolution_chain[str(i)]
    if isinstance(temp, list):
        evolution_chain[str(i)] = [pokemon for pokemon in temp if pokemon in another_pkmlist]
    else:
        if temp not in another_pkmlist:
            del evolution_chain[str(i)] 



n = 1
for i in range(1, len(evolution_chain)+1):

    """
        Linking the right evolution-chain to the right pokemons

        Because of the structure of the evolution chain data,
        we use both i and n to move through the different data.

        i = for the evolution chains
        n = for the pokemon

        n needs to increment for every single pokemon and we do this with 4 if's
        since there are at most 4 evolutions.
        This is dont so we are able to correctly increment n 
    """

    try:
        if poke_data[str(n)]["name"] in evolution_chain[str(i)]:
            poke_data[str(n)]["evolution-chain"] = str(i)
            n += 1

            if poke_data[str(n)]["name"] in evolution_chain[str(i)]:
                poke_data[str(n)]["evolution-chain"] = str(i)
                n += 1

                if poke_data[str(n)]["name"] in evolution_chain[str(i)]:
                    poke_data[str(n)]["evolution-chain"] = str(i)
                    n += 1
                
                    if poke_data[str(n)]["name"] in evolution_chain[str(i)]:
                        poke_data[str(n)]["evolution-chain"] = str(i)
                        n += 1
        else:
            n += 1
    except:
        pass



"""
    Now to store our data in json files to later be added into a SQLite database

    pokedex_gen1.json:
        - stores data on every pokemon in the pokedex

    evolutionChains.json:
        - stores data on the evolution chains for each pokemon
"""


with open("data/pokedex_gen1.json", "w") as json_file:
    json.dump(poke_data, json_file, indent=4)

with open("data/evolutionChains.json", "w") as json_file:
    json.dump(evolution_chain, json_file, indent=4)