from project import app
from flask import redirect, url_for, render_template, request
from project.models.Search import *
from project.models.Pokedex import *
from project.models.Pokemon import *

# search function used when on Pokedex page
@app.route("/<username>/pokedex/search")
def pokedex_search(username):
    q = request.args.get('q').lower()
    if pokemon_exist(q):
        return redirect(url_for("pokemon_page", username=username, name=q))
    else:
        error_message = "Couldn't find Pokemon"
        pokemons = all_pokemons()
        return render_template("pokedex.html", username=username, pokemons=pokemons, error_message=error_message)

# search function used when on Pokemon page
@app.route("/<username>/pokedex/<current>/search")
def pokemon_search(username, current):
    q = request.args.get("q").lower()
    if pokemon_exist(q):
        return redirect(url_for("pokemon_page", username=username, name=q))
    else:
        error_message = "Couldn't find Pokemon"
        pkm = find_pokemon(current)
        # if id < 3 make sure to add zeros to it looks nice on the webpage
        if len(str(pkm[0])) < 3:
            pkm = [str(pkm[0]).zfill(3),] + pkm[1:]

        # Check if damage multiplyer exists
        has_4x_damage, has_2x_damage, has_1x_damage, has_05x_damage, has_025x_damage, has_0x_damage = check_damage(pkm)
        
        return render_template(
            "pokemon.html", pkm=pkm, has_4x_damage=has_4x_damage, has_2x_damage=has_2x_damage,
            has_1x_damage=has_1x_damage, has_05x_damage=has_05x_damage,
            has_025x_damage=has_025x_damage, has_0x_damage=has_0x_damage, username=username, error_message=error_message
        )
