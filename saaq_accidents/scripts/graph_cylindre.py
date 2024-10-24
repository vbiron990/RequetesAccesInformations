import pandas as pd
import matplotlib.pyplot as plt
import os

# Charger le fichier CSV dans un DataFrame pandas
path_script = os.path.dirname(os.getcwd())
data_path = os.path.join(path_script, 'saaq_accidents', 'data', 'raw', 'data.csv')
data = pd.read_csv(data_path)

# Créer un sous-ensemble des données avec uniquement les colonnes pertinentes
subset = data[['Nature des dommages', 'Cylindré']]

# Grouper les données par la nature des dommages et calculer la moyenne de la cylindrée
grouped_data = subset.groupby('Nature des dommages')['Cylindré'].mean()

# Créer un graphique à barres pour montrer la corrélation entre la nature des dommages et la cylindrée
plt.figure(figsize=(8, 6))
grouped_data.plot(kind='bar', color='skyblue')
plt.title('Corrélation entre la nature des dommages et la cylindrée')
plt.xlabel('Nature des dommages')
plt.ylabel('Cylindrée moyenne')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()

# Enregistrer le graphique en tant qu'image au format PNG
plt.savefig('graph_cylindre.png')

# Afficher le graphique
plt.show()