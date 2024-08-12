import streamlit as stl 

import pandas as pd

import plotly.express as px

import seaborn as sns

stl.set_page_config(page_title='Titanic',page_icon=':bar_chart',layout='wide')

stl.title("My titanic Dashboard1")

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




    rrange = [0,12,18,35,60,100]
    labels = ['child','Teenager','Yount Adul','Adult','Senior']
    df['Age Group']=pd.cut(df["Age"],bins=rrange,labels=labels)
    survival_rate=df.groupby(['Age Group','Sex'])['Survived'].mean().reset_index()
    survival_rate.columns=['Age Group','Sex','Survival Rate']
    

    customer_colors = ['#FFD23F','#337357']

    fig = px.bar(survival_rate,x='Age Group',y='Survival Rate',color='Sex',
                 barmode='stack',color_discrete_sequence=customer_colors,
                 text='Survival Rate',
                 title="Survival Rate by Age Group Sex"
                 )
    fig.update_traces(texttemplate="%{text:.2f}",textposition='inside')
    stl.plotly_chart(fig)

    customer_colors = ['#FFD23F','#337357']

    fig_scotter=px.scatter(df,y='Age',x='Sex',color='Sex',)
    stl.plotly_chart(fig_scotter)

    scatter_plot = sns.scatterplot(data=df,x='Survived',y='Age',hue='Sex')
    stl.pyplot(scatter_plot.figure)

    survival_rate=df.pivot_table(values='Survived',index='Pclass',columns='Embarked',aggfunc='mean')
    stl.dataframe(survival_rate)


        
    

    