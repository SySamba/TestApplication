import streamlit as stl 

import pandas as pd

stl.set_page_config(page_title='Titanic',page_icon=':bar_chart',layout='wide')

stl.title("My titanic Dashboard")

@stl.cache_data
def loadDataset(inputfile):
    data =  pd.read_csv(inputfile)
    return data 

inputFile = stl.sidebar.file_uploader('Ulpload your file',
                              type =['csv'])




if inputFile is not None :
    df = loadDataset(inputFile)

    columns = stl.multiselect("Select columns",df.columns)

    rows = stl.slider('Please select a number of rows',5,len(df))

    with stl.expander("Expand to view the data"):
        stl.write(df[columns].head(rows))

    stl.write("Number of male and  females")
    select_embarqued = stl.selectbox("select Embarkation",options=["All"]+
                                     list(df["Embarked"].dropna().unique()))
    col1,col2=stl.columns(2)

    if select_embarqued=='All':
        filterData=df
    else:
        filterData=df[df["Embarked"]==select_embarqued]

    with col1:
        stl.write("Number of Male and females")
        gendar_embar_Count=filterData["Sex"].value_counts()
        stl.bar_chart(gendar_embar_Count) 
    with col2 :
        gendar_embar_Count=filterData["Sex"].value_counts()
        embar_sur=filterData[df['Survived']==1]
        embar_sur_count=embar_sur["Sex"].value_counts()
        embar_sur_per=(embar_sur_count/gendar_embar_Count)*100
        stl.bar_chart(embar_sur_per)


        
    

    