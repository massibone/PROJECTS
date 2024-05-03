import json
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Apri il file JSON in modalità lettura
with open('dataset.json', 'r') as f:
    # Carica il contenuto del file JSON in un oggetto Python
    data = json.load(f)

# Creazione del DataFrame utilizzando la lista di record di traffico
df = pd.DataFrame(data['traffic_records'])

# Verifica dei valori mancanti in ogni colonna
missing_cols = df.columns[df.isna().any()]

# Gestione dei valori mancanti
for col in missing_cols:
    if df[col].dtype == 'float64' or df[col].dtype == 'int64':
        df[col] = df[col].fillna(df[col].mean())
    elif df[col].dtype == 'object':
        df.dropna(subset=[col], inplace=True)

# Identificazione delle colonne categoriali
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

# Codifica delle variabili categoriali utilizzando OneHotEncoder
encoder = OneHotEncoder(handle_unknown="ignore")
encoded_data = encoder.fit_transform(df[categorical_cols])

# Creazione di un DataFrame per i dati codificati
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_cols))


# Eliminazione delle colonne categoriali dal DataFrame originale
df.drop(columns=categorical_cols, inplace=True)

# Concatenazione dei DataFrame codificati e originale
df = pd.concat([df, encoded_df], axis=1)

# Salvataggio del DataFrame pre-elaborato come file JSON
df.to_json('preprocessed_data.json', orient='records')
