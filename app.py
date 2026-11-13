import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Configuration de la page mobile/PC
st.set_page_config(page_title="Suivi Instantané", page_icon="💧", layout="wide")

# Rafraîchissement automatique toutes les 60 secondes (60000 ms)
st_autorefresh(interval=60000, key="refresh_eau")

# Lien direct CSV publié sur le web
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRJQ7tPFcVCCU394BEMlGOdfJZ5qCrtv-zj8IDLwpfBOaum7lcmKY-VY-Da20dbR0elgCI33vVJGP5v/pub?gid=1866023781&single=true&output=csv"

st.title("💧 Suivi Instantané des Compteurs")

try:
    # Lecture directe des données du Sheet
    df = pd.read_csv(URL_CSV)
    
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
    st.error(f"Impossible de lire le Google Sheet : {e}")
