import streamlit as st
import pandas as pd

# URLs des fichiers CSV
url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url_deaths    = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

# Télécharger et charger les données directement
df_confirmed = pd.read_csv(url_confirmed)
df_deaths = pd.read_csv(url_deaths)
df_recovered = pd.read_csv(url_recovered)

# Visualisation simple pour vérifier le chargement des données
st.title("Analyse Mondiale COVID-19")

st.subheader("Aperçu des Cas Confirmés")
st.dataframe(df_confirmed.head())

st.subheader("Aperçu des Décès")
st.dataframe(df_deaths.head())

st.subheader("Aperçu des Personnes Soignées")
st.dataframe(df_recovered.head())
