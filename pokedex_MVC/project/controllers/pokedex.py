from project import app
from flask import render_template
from project.models.Pokedex import *

# main pokedex
@app.route("/<username>/pokedex")
def pokedex(username):
    pokemons = all_pokemons()
    return render_template("pokedex.html", username=username, pokemons=pokemons)