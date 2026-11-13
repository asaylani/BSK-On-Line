import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Configuration de la page mobile/PC
st.set_page_config(page_title="Suivi Instantané", page_icon="💧", layout="wide")

# Rafraîchissement automatique toutes les 60 secondes (60000 ms)
st_autorefresh(interval=60000, key="refresh_eau")

# Lien direct vers le fichier poussé sur GitHub
PSEUDO_GITHUB = "asaylani"
URL_CSV = f"https://raw.githubusercontent.com/{PSEUDO_GITHUB}/suivi-eau/main/donnees.csv"

st.title("💧 Suivi Instantané des Compteurs")

try:
    # Lecture directe des données (séparateur point-virgule)
    df = pd.read_csv(URL_CSV, sep=";")
    
    # Création d'une carte visuelle (objet metric) par ligne
    cols = st.columns(len(df))
    for i, row in df.iterrows():
        with cols[i]:
            val = row['VALEUR']
            horodatage = row['DERNIERE_MODIF'] if 'DERNIERE_MODIF' in df.columns else ""
            st.metric(
                label=f"{row['DESCRIPTION']} ({row['SIGNAL']})",
                value=f"{val}",
                delta=f"Maj : {horodatage}"
            )
            
    st.divider()
    st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Impossible de lire les données : {e}")
