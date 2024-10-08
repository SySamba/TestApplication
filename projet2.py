import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Tableau de Bord COVID-19", page_icon="🌍", layout="wide")

# Bannière d'en-tête
st.markdown("""
    <div style="background-color:#1a73e8;padding:15px;border-radius:10px;text-align:center;">
    <h1 style="color:white;">🌍 Tableau de Bord Mondial COVID-19</h1>
    </div>
    """, unsafe_allow_html=True)

# Chargement des données avec mise en cache
@st.cache_data
def load_data():
    df_confirmed = pd.read_csv('time_series_covid19_confirmed_global.csv')
    df_deaths = pd.read_csv('time_series_covid19_deaths_global.csv')
    df_recovered = pd.read_csv('time_series_covid19_recovered_global.csv')
    
    # Convertir les colonnes en types appropriés pour optimiser
    df_confirmed.iloc[:, 4:] = df_confirmed.iloc[:, 4:].astype('int32')
    df_deaths.iloc[:, 4:] = df_deaths.iloc[:, 4:].astype('int32')
    df_recovered.iloc[:, 4:] = df_recovered.iloc[:, 4:].astype('int32')
    
    return df_confirmed, df_deaths, df_recovered

df_confirmed, df_deaths, df_recovered = load_data()

# Fonction pour transformer les données de format large à long
def melt_data(df, value_name):
    df_melted = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                        var_name='Date', value_name=value_name)
    df_melted['Date'] = pd.to_datetime(df_melted['Date'])
    return df_melted

# Appliquer la transformation aux trois jeux de données
df_confirmed_long = melt_data(df_confirmed, 'Confirmed')
df_deaths_long = melt_data(df_deaths, 'Deaths')
df_recovered_long = melt_data(df_recovered, 'Recovered')

# Fusionner les datasets confirmés, décès et guérisons
df_merged = df_confirmed_long.merge(df_deaths_long[['Country/Region', 'Date', 'Deaths']],
                                    on=['Country/Region', 'Date'], how='left')
df_merged = df_merged.merge(df_recovered_long[['Country/Region', 'Date', 'Recovered']],
                            on=['Country/Region', 'Date'], how='left')

# Gestion de la barre latérale pour sélectionner un pays
st.sidebar.title('Tableau de Bord COVID-19')
country_list = df_merged['Country/Region'].unique()
selected_country = st.sidebar.selectbox('Sélectionnez un pays', country_list)

# Filtrer les données en fonction du pays sélectionné
df_country = df_merged[df_merged['Country/Region'] == selected_country]

# Design des statistiques avec des cartes
st.markdown(f"<h2 style='text-align:center;color:#333;'>Analyse COVID-19 : {selected_country}</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# CSS pour cartes de la même taille
card_css = """
    <style>
    .card {
        background-color: #F4F6F9;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        width: 100%;
        height: 150px;
    }
    .card h3 {
        color: #333;
        font-size: 18px;
    }
    .card p {
        font-size: 25px;
        color: #333;
    }
    </style>
    """
st.markdown(card_css, unsafe_allow_html=True)

# Utilisation de la classe 'card' pour les cartes avec icônes
col1.markdown(f"""
    <div class="card">
        <h3 style="color:#ff6347;">🦠 Cas Confirmés</h3>
        <p>{df_country['Confirmed'].max():,}</p>
    </div>
    """, unsafe_allow_html=True)

col2.markdown(f"""
    <div class="card">
        <h3 style="color:#FF4500;">☠️ Décès</h3>
        <p>{df_country['Deaths'].max():,}</p>
    </div>
    """, unsafe_allow_html=True)

col3.markdown(f"""
    <div class="card">
        <h3 style="color:#2E8B57;">💊 Guérisons</h3>
        <p>{df_country['Recovered'].max():,}</p>
    </div>
    """, unsafe_allow_html=True)

# Visualisation des tendances temporelles
st.markdown(f"### Tendances des Cas, Décès et Guérisons au {selected_country}")
fig = px.line(df_country, x='Date', y=['Confirmed', 'Deaths', 'Recovered'],
              labels={'value': 'Nombre', 'Date': 'Date'},
              title=f"Tendances des Cas Confirmés, Décès et Guérisons au {selected_country}",
              template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Comparaison des cas confirmés et des décès pour plusieurs pays
st.sidebar.subheader('Comparaison entre pays')
selected_countries = st.sidebar.multiselect('Sélectionnez les pays à comparer', country_list)

if selected_countries:
    df_compare = df_merged[df_merged['Country/Region'].isin(selected_countries)]
    
    st.markdown("### Comparaison des Cas Confirmés entre les Pays Sélectionnés")
    fig_compare = px.line(df_compare, x='Date', y='Confirmed', color='Country/Region',
                          title='Comparaison des Cas Confirmés',
                          template="plotly_dark")
    st.plotly_chart(fig_compare, use_container_width=True)
    
    st.markdown("### Comparaison des Décès entre les Pays Sélectionnés")
    fig_compare_deaths = px.line(df_compare, x='Date', y='Deaths', color='Country/Region',
                                 title='Comparaison des Décès',
                                 template="plotly_dark")
    st.plotly_chart(fig_compare_deaths, use_container_width=True)

# Analyse Globale avec regroupement par mois et mise en cache pour optimiser les performances
@st.cache_resource
def get_global_data():
    # Grouper les données par mois pour optimiser les performances
    df_global = df_merged.groupby(pd.Grouper(key='Date', freq='M')).sum().reset_index()
    return df_global

if st.sidebar.button('Voir les tendances globales'):
    df_global = get_global_data()

    st.markdown("### Tendances Globales des Cas Confirmés, Décès et Guérisons (Mois Derniers)")
    fig_global = px.line(df_global, x='Date', y=['Confirmed', 'Deaths', 'Recovered'],
                         title='Tendances Mondiales des Cas Confirmés, Décès et Guérisons (Par Mois)',
                         template="ggplot2")
    st.plotly_chart(fig_global, use_container_width=True)

# Ajouter du CSS pour le styling général
st.markdown("""
<style>
body {
    background-color: #f0f2f5;
}
h1, h2, h3 {
    color: #1a73e8;
}
.sidebar .sidebar-content {
    background-color: #ffffff;
}
.metric {
    text-align: center;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)
