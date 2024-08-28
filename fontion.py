import streamlit as stl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px






df= pd.read_csv('exo.csv')

stl.write(df)






fig = sns.scatterplot(data=df, x='fractionalDeathYear' , y='Age', hue='PlaceofDeath')

stl.pyplot(fig.figure)

stl.write('Place of Death')


place_of_death = df['PlaceofDeath'].value_counts().reset_index()

fig = px.pie(place_of_death,names='PlaceofDeath',values='count',
             title='Percentage of place of death')

stl.plotly_chart(fig)