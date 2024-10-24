import pandas as pd
import matplotlib.pyplot as plt
import os

# Charger le fichier CSV contenant vos données
path_script = os.path.dirname(os.getcwd())
data_path = os.path.join(path_script, 'saaq_accidents', 'data', 'raw', 'data.csv')
output_path = os.path.join(path_script, 'saaq_accidents', 'output', 'graph_type_vehicule_bus_scolaires.png')
data = pd.read_csv(data_path)

# Filtrer les données pour les types de dommages 'Graves' et 'Mortels'
dommages_graves = data[data['Nature des dommages'] == 'Graves']
dommages_mortels = data[data['Nature des dommages'] == 'Mortels']

# Filtrer les données pour les types de véhicule 'Automobile', 'Camionnette', 'VUS' et 'Autobus scolaire'
types_vehicules_inclus = ['Automobile', 'Camionnette', 'VUS', 'Autobus scolaire']
filtered_data = data[data['Type de véhicule'].isin(types_vehicules_inclus)]

# Filtrer les données des dommages 'Graves' et 'Mortels' pour ces types de véhicule
dommages_graves_filtres = dommages_graves[dommages_graves['Type de véhicule'].isin(types_vehicules_inclus)]
dommages_mortels_filtres = dommages_mortels[dommages_mortels['Type de véhicule'].isin(types_vehicules_inclus)]

# Compter le nombre de dommages graves par type de véhicule
graves_par_type_vehicule = dommages_graves_filtres.groupby('Type de véhicule')['Nature des dommages'].count()

# Compter le nombre de dommages mortels par type de véhicule
mortels_par_type_vehicule = dommages_mortels_filtres.groupby('Type de véhicule')['Nature des dommages'].count()

# Créer un DataFrame pour la comparaison
comparaison = pd.DataFrame({
    'Graves': graves_par_type_vehicule,
    'Mortels': mortels_par_type_vehicule
})

# Calcul du rapport Mortels/Graves
comparaison['Rapport Mortels/Graves'] = comparaison['Mortels'] / comparaison['Graves']

# Créer un graphique à barres pour représenter le rapport Mortels/Graves par type de véhicule
ax = comparaison['Rapport Mortels/Graves'].plot(kind='bar', figsize=(10, 6), color='skyblue')
plt.title("Rapport Mortels vs Graves par type de véhicule")
plt.xlabel("Type de véhicule")
plt.ylabel("Rapport Mortels/Graves")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()

# Limiter l'affichage aux types de véhicules spécifiés
ax.set_xticklabels(comparaison.index)

# Enregistrer le graphique en tant qu'image au format PNG
plt.savefig(output_path)

# Afficher le graphique
plt.show()
