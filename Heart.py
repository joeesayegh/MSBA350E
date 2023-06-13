import streamlit as st
import pandas as pd
import plotly.express as px
import hydralit_components as hc 

# Load and preprocess the data
df = pd.read_csv('heart.csv')
st.set_page_config(layout="wide", page_title=None)
# Perform any necessary preprocessing steps here

# Create individual visualizations
age_hist = px.histogram(df, x='age', nbins=20, title='Age Distribution')
sex_pie = px.pie(df, names='sex', title='Gender Distribution')
chest_pain_bar = px.bar(df['cp'].value_counts(), title='Chest Pain Types')
# Add more visualizations for other features

# Set up the Streamlit app
st.title('Heart Disease Dashboard')

# Create a grid layout
col1, col2 = st.columns([1, 2])
col3, col4 = st.columns([1, 2])

# Display visualizations in the first row
col1.subheader('Age Distribution')
with col1:
    st.plotly_chart(age_hist)

col2.subheader('Gender Distribution')
with col2:
    st.plotly_chart(sex_pie)

# Display visualizations in the second row
col3.subheader('Chest Pain Types')
with col3:
    st.plotly_chart(chest_pain_bar)

# Display additional visualizations in the second row
# Example: Resting Blood Pressure - Histogram
rest_bp_hist = px.histogram(df, x='trestbps', nbins=20, title='Resting Blood Pressure Distribution')
col4.subheader('Resting Blood Pressure Distribution')
with col4:
    st.plotly_chart(rest_bp_hist)

col5,col6,col7,col8 = st.columns([3,3,3,3])
with col5:
    st.markdown("Heart Diseases")
    theme_vacc = {'bgcolor':'#EFF8F7','content_color':'navy','progress_color':'navy'}
        #Info Cards for vaccinations
     
    hc.info_card(title="Females", bar_value=int(df["sex"].eq(1).sum()), content=int(df["sex"].eq(1).sum()), theme_override=theme_vacc)
    hc.info_card(title="Males", bar_value=int(df["sex"].eq(0).sum()), content=int(df["sex"].eq(0).sum()), theme_override=theme_vacc)

