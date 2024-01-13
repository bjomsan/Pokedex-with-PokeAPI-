# Pokedex-with-PokeAPI
!NB! work in progress

I have used PokeAPI(https://pokeapi.co/) to create a Pokdex MVC with Flask. 
The application contains:
- **Login/register**: the first page requires the user to login to an existing account or create a new one.
- **Pokedex**: The main pokedex. Overwies over all pokemons.
- **Pokemon info**: Each pokemon has its own page with detailes info about stats/weaknesses/evolutions
- **Search bar**: Both Pokedex- and Pokemon page has a searchbar were the user can search for a pokemon.

## Flders/Files

- **datagathering**
  - These programs calls the api, manipulates the data I want and stores them in a sqlite database.
  "data" is a folder with json-data on thep pokemons before its inserted to the database.
  
- **pokedex_MVC**
  - **Models**: Every model have correlated controller.
  - **Controllers**: Every controller have correlated model.
  - **Templates**: Views, html documents
  - **Static**: css and fonts
  - **weakness_calculator**: a program that calculates damage taken from all pokemon types.

 ### Images of the GUI/HTML
![pokedex](https://github.com/bjomsan/Pokedex-with-PokeAPI-/assets/124776049/6b9419ec-4eaa-4967-b5cf-bb726a4bb5e8)
![pokemon](https://github.com/bjomsan/Pokedex-with-PokeAPI-/assets/124776049/764e3c76-28bd-400d-9acf-23ca52ffdad8)
