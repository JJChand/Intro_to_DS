import pandas as pd #type: ignore

poke = pd.read_csv('pokemon_data.csv')

print(poke.tail(5))

