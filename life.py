import streamlit as st
import plotly.express as px
import pandas as pd

# Load the life expectancy data from your dataframe
df = pd.read_csv('Life-Expectancy-Data-Updated.csv')

st.set_page_config(layout="wide", page_title=None)

# Get the minimum and maximum years
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

# Set the title of the web app
st.title('Life Expectancy Map')

# Add a slider for selecting the year
selected_year = st.slider('Select Year', min_value=min_year, max_value=max_year)

# Filter the data based on the selected year
filtered_df = df[df['Year'] == selected_year]

# Create a figure using Plotly Express
fig = px.choropleth(filtered_df, 
                    locations='Country', 
                    locationmode='country names',
                    color='Life_expectancy',
                    hover_name='Country',
                    title='Life Expectancy by Country')

# Set the range of colors for the color scale
fig.update_layout(coloraxis_colorbar=dict(title='Life Expectancy'))

# Show the figure using Streamlit
st.plotly_chart(fig)
