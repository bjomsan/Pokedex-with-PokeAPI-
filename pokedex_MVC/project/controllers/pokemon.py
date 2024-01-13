from project import app
from flask import render_template
from project.models.Pokemon import *

# pokemon page
@app.route("/<username>/pokedex/<name>")
def pokemon_page(username, name):
    pkm = find_pokemon(name)
    # if id < 3 make sure to add zeros to it looks nice on the webpage
    if len(str(pkm[0])) < 3:
        pkm = [str(pkm[0]).zfill(3),] + pkm[1:]

    # Check if damage multiplyer exists
    has_4x_damage, has_2x_damage, has_1x_damage, has_05x_damage, has_025x_damage, has_0x_damage = check_damage(pkm)
    
    return render_template(
        "pokemon.html", pkm=pkm, has_4x_damage=has_4x_damage, has_2x_damage=has_2x_damage,
        has_1x_damage=has_1x_damage, has_05x_damage=has_05x_damage,
        has_025x_damage=has_025x_damage, has_0x_damage=has_0x_damage, username=username
    )