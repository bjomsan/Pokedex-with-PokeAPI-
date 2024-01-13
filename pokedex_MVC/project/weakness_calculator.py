def find_weakness(curr_pkm_type):
    # the valeus of each key is a dict were keys are type and
    # values are how much dmg the type does to the parent key.
    # soruce: https://pokemondb.net/type
    damage_chart = {
    "normal": {"fighting": 2.0, "ghost": 0},
    "fire": {"fire": 0.5, "water": 2.0, "grass": 0.5, "ice": 0.5, "ground": 2.0, "bug": 0.5, "rock": 2.0, "steel": 0.5, "fairy": 0.5},
    "water": {"fire": 0.5, "water": 0.5, "electric": 2.0, "grass": 2.0, "ice": 0.5, "steel": 0.5},
    "electric": {"electric": 0.5, "ground": 2.0, "flying": 0.5, "steel": 0.5},
    "grass": {"fire": 2.0, "water": 0.5, "grass": 0.5, "ice": 2.0, "poison": 2.0, "ground": 0.5, "flying": 2.0, "bug": 2.0},
    "ice": {"fire": 2.0, "ice": 0.5, "fighting": 2.0, "rock": 2.0, "steel": 2.0},
    "fighting": {"flying": 2.0, "psychic": 2.0, "bug": 0.5, "rock": 0.5, "dark": 0.5, "fairy": 2.0},
    "poison": {"grass": 0.5, "fighting": 0.5, "poison": 0.5, "ground": 2.0, "psychic": 2.0, "fairy": 0.5},
    "ground": {"water": 2.0, "electric": 0.0, "grass": 2.0, "ice": 2.0, "poison": 1/2.0, "rock": 0.5},
    "flying": {"electric": 2.0, "grass": 0.5, "ice": 2.0, "fighting": 0.5, "ground": 0.0, "bug": 0.5, "rock": 2.0},
    "psychic": {"fighting": 0.5, "psychic": 0.5, "bug": 2.0, "ghost": 2.0, "dark": 2.0},
    "bug": {"fire": 2.0, "grass": 0.5, "fighting": 0.5, "ground": 0.5, "flying": 2.0, "rock": 2.0},
    "rock": {"normal": 0.5, "fire": 0.5, "water": 2.0, "grass": 2.0, "fighting": 2.0, "poison": 0.5, "ground": 2.0, "flying": 0.5, "steel": 2.0},
    "ghost": {"normal": 0.0, "fighting": 0.0, "poison": 0.5, "bug": 0.5, "ghost": 2.0, "dark": 2.0},
    "dragon": {"fire": 0.5, "water": 0.5, "electric": 0.5, "grass": 0.5, "ice": 2.0, "dragon": 2.0, "fairy": 2.0},
    "dark": {"fighting": 2.0, "psychic": 0.0, "bug": 2.0, "ghost": 0.5, "dark": 0.5, "fairy": 2.0},
    "steel": {"normal": 0.5, "fire": 2.0, "grass": 0.5, "ice": 0.5, "fighting": 2.0, "poison": 0.0, "ground": 2.0, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 0.5, "dragon": 0.5, "steel": 0.5, "fairy": 0.5},
    "fairy": {"fighting": 0.5, "poison": 2.0, "bug": 0.5, "dragon": 0.0, "dark": 0.5, "steel": 2.0}
    }

    # base case is 1 on all types.
    base_chart = {
        "normal": 1, "fire": 1, "water": 1, "electric": 1, "grass": 1, "ice": 1,
        "fighting": 1, "poison": 1, "ground": 1, "flying": 1, "psychic": 1, "bug": 1,
        "rock": 1, "ghost": 1, "dragon": 1, "dark": 1, "steel": 1, "fairy": 1
        }


    for type in curr_pkm_type:
        # find damage taken from different types
        temp1 = damage_chart[type] 

        for key, val in temp1.items():
            # for each type, multiply with base case
            temp2 = base_chart[key] * val
            base_chart[key] = temp2
            
    return base_chart