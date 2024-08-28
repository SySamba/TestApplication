import pandas as pd

# Spécifiez le chemin vers votre fichier Parquet
file_path = "data.parquet"

# Chargez le dataset dans un DataFrame Pandas
df = pd.read_parquet(file_path)

# Affichez les premières lignes pour vérifier le chargement
print(df.head())



