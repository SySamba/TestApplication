import streamlit as stl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


stl.set_page_config(page_title='Analyse des Décès', page_icon=':bar_chart:', layout='wide')


stl.markdown("""
    <style>
    body {
        background-color: #f7f9fc;
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
    }
    .reportview-container .main .block-container{
        padding: 1rem;
    }
    h1 {
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #34495e;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 10px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #34495e;
        color: #ecf0f1;
    }
    .stMarkdown {
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)


stl.markdown("<h1 style='text-align: center;'>Dashboard d'Analyse des Décès</h1>", unsafe_allow_html=True)


@stl.cache_data
def loadDataset(inputfile):
    data = pd.read_csv(inputfile)
    return data


inputFile = stl.sidebar.file_uploader('Téléchargez votre fichier CSV', type=['csv'])


if inputFile is not None:
    df = loadDataset(inputFile)

    
    stl.markdown("### Contrôles de Sélection", unsafe_allow_html=True)

    
    stl.markdown("#### Sélectionnez les colonnes à afficher", unsafe_allow_html=True)
    columns = stl.multiselect("", df.columns.tolist())
    stl.markdown("<br>", unsafe_allow_html=True)  

   
    stl.markdown("#### Sélectionnez le nombre de lignes à afficher", unsafe_allow_html=True)
    rows = stl.slider('', 5, len(df), 10)
    stl.markdown("<br>", unsafe_allow_html=True)  

    
    stl.markdown("#### Sélectionnez le lieu de décès", unsafe_allow_html=True)
    select_place_of_death = stl.selectbox("", options=["All"] + list(df["PlaceofDeath"].dropna().unique()))
    stl.markdown("<br>", unsafe_allow_html=True)  
    
    if select_place_of_death == 'All':
        filterData = df
    else:
        filterData = df[df["PlaceofDeath"] == select_place_of_death]

    
    if columns:
        with stl.expander("Aperçu des données filtrées"):
            stl.dataframe(filterData[columns].head(rows).style.set_table_styles(
                [{'selector': 'th', 'props': [('background-color', '#f2f2f2')]}]
            ))
    else:
        stl.warning("Sélectionnez des colonnes pour afficher les données.")

    
    stl.markdown("---")  
    stl.markdown("### Visualisations")


    # Analyse de l'Âge et du Sexe
    stl.markdown("#### Distribution des Âges par Lieu de Décès")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filterData, x='fractionalDeathYear', y='Age', hue='gender', palette='Set2', ax=ax)
    ax.set_title('Répartition des Âges par Année Fractionnelle', fontsize=14)
    ax.set_xlabel('Année Fractionnelle')
    ax.set_ylabel('Âge')
    ax.grid(True)
    stl.pyplot(fig)


    # Analyse du Lieu de Décès 
    stl.markdown("#### Répartition des Décès par Lieu")
    place_of_death = df['PlaceofDeath'].value_counts().reset_index()
    place_of_death.columns = ['PlaceofDeath', 'count']

    fig = px.pie(place_of_death, names='PlaceofDeath', values='count',
                 title='Pourcentage des Lieux de Décès',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    stl.plotly_chart(fig, use_container_width=True)



    # Analyser les dates de décès pour identifier des pics ou des motifs temporels
    stl.markdown("### Analyse Temporelle")
    df['DateofDeath'] = pd.to_datetime(df['DateofDeath'])
    deaths_over_time = df.groupby(df['DateofDeath'].dt.date).size().reset_index(name='count')

    fig = px.line(deaths_over_time, x='DateofDeath', y='count',
              title='Nombre de Décès au Fil du Temps',
              labels={'DateofDeath': 'Date de Décès', 'count': 'Nombre de Décès'})
    stl.plotly_chart(fig, use_container_width=True)



    # Analyser les décès par année
    stl.markdown("### Tendances Années par Années")
    deaths_per_year = df.groupby('yearOfDeath').size().reset_index(name='count')

    fig = px.bar(deaths_per_year, x='yearOfDeath', y='count',
             title='Nombre de Décès par Année',
             labels={'yearOfDeath': 'Année de Décès', 'count': 'Nombre de Décès'},
             color='count', color_continuous_scale='Viridis')
    stl.plotly_chart(fig, use_container_width=True)



    # Comparer les décès selon les tranches d'âge
    stl.markdown("### Analyse par Tranche d'Âge")
    age_bracket_deaths = df['ageBracket'].value_counts().reset_index()
    age_bracket_deaths.columns = ['ageBracket', 'count']

    fig = px.bar(age_bracket_deaths, x='ageBracket', y='count',
             title='Nombre de Décès par Tranche d\'Âge',
             labels={'ageBracket': 'Tranche d\'Âge', 'count': 'Nombre de Décès'},
             color='count', color_continuous_scale='Blues')
    stl.plotly_chart(fig, use_container_width=True)



    # Détection d'anomalies dans les taux de mortalité
    stl.markdown("### Détection d'Anomalies")
    fig = px.box(df, x='yearOfDeath', y='Age', color='gender',
             title='Distribution des Âges par Année avec Anomalies',
             labels={'yearOfDeath': 'Année de Décès', 'Age': 'Âge'},
             color_discrete_map={'Male': 'blue', 'Female': 'red'})
    stl.plotly_chart(fig, use_container_width=True)

    
    stl.markdown("<hr><p style='text-align: center; color: #95a5a6;'>Samba SY étudiant Master 2 Business Intelligence (BI) à l'UCAD❤️ </p>", unsafe_allow_html=True)
