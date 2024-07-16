import pandas as pd

# Charger le fichier CSV dans un DataFrame
df = pd.read_csv('emissions.csv')

# Extraire les noms d'états uniques
unique_states = df['state-name'].unique()

# Convertir en DataFrame
unique_states_df = pd.DataFrame(unique_states, columns=['state-name'])

# Sauvegarder dans un nouveau fichier CSV
unique_states_df.to_csv('state_names.csv', index=False)

print("Unique state names have been saved to output.csv")
