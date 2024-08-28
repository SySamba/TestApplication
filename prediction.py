import pandas as pd
import streamlit as stl
import plotly.express as px

stl.set_page_config(page_title='Prediction', page_icon=':bar_chart:', layout='wide')

stl.title("My Prediction")

@stl.cache_data
def loadDataset(inputfile):
    data = pd.read_csv(inputfile)
    return data

inputFile = stl.sidebar.file_uploader('Upload your file', type=['csv'])

if inputFile is not None:
    df = loadDataset(inputFile)

    option = stl.sidebar.radio("Menu", ["Analyse descriptive", "Prediction", "NLP"])

    if option == "Analyse descriptive":
        stl.write("Welcome to the analyst page")
        nbre_of_event = df.shape[0]

        stl.markdown(
            f'''
            <div style="background-color:#F9DBBA; padding:10px; border-radius:5px; text-align:center;">
                <h4 style="color:#5B99C2; text-align:center;">Card Title</h4>
                <h5 style="color:#5B99C2; text-align:center;">Number of Events</h5>
                <p style="color:#1F316F; text-align:center;">{nbre_of_event}<p>
            </div>
            ''',
            unsafe_allow_html=True
        )

        df['timeStamp'] = pd.to_datetime(df["timeStamp"])

        df['Hour'] = df["timeStamp"].dt.hour
        hourly_call = df.groupby('Hour').size().reset_index(name="counts")
        #stl.write(hourly_call)
        fig = px.line(hourly_call, x='Hour', y='counts', title='911 Calls by Hours')
        stl.plotly_chart(fig)

        df['Days of week'] = df['timeStamp'].dt.day_of_week

        # Mapping des jours de la semaine
        days_map = {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi', 5: 'Samedi', 6: 'Dimanche'}
        df['Days of week'] = df['Days of week'].map(days_map)

        # Transformer la colonne en catégorie ordonnée
        ordered_days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        df['Days of week'] = pd.Categorical(df['Days of week'], categories=ordered_days, ordered=True)

        # Trier le DataFrame
        week_hourly_cal = df.groupby('Days of week').size().reset_index(name='counts').sort_values('Days of week')
        
        fig = px.bar(week_hourly_cal, x='Days of week', y='counts', title='911 Calls by Day of the Week')
        stl.plotly_chart(fig)

    elif option == "Prediction":
        stl.write("Welcome to the prediction page")

    else:
        stl.write("Welcome to the NLP page")
