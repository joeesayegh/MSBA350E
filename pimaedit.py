# Importing the Libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import hydralit_components as hc
import plotly.graph_objects as go
import plotly.colors as colors


# Importing the datasets
df1 = pd.read_csv("annual-number-of-deaths-by-cause.csv")
df2 = pd.read_csv("total-cancer-deaths-by-type.csv")
df3 = pd.read_csv("cancer-deaths-by-age.csv")
df4 = pd.read_csv("cancer-death-rates-by-age.csv")
df5 = pd.read_csv("share-of-population-with-cancer.csv")
df6 = pd.read_csv("number-of-people-with-cancer-by-age.csv")
df7 = pd.read_csv("share-of-population-with-cancer-by-age.csv")
df8 = pd.read_csv("cancer-death-rates.csv")
df9 = pd.read_csv("cancer-death-rates-by-type.csv")
df10 = pd.read_csv("lung-cancer-deaths-per-100000-by-sex-1950-2002.csv")
df11 = pd.read_csv("sales-of-cigarettes-per-adult-per-day.csv")
df12 = pd.read_csv("share-of-cancer-deaths-attributed-to-tobacco.csv")
df13 = pd.read_csv("cancer-death-rates-in-the-us.csv")
df14 = pd.read_csv("cancer-deaths-rate-and-age-standardized-rate-index (1).csv")

# Settings streamlit page configuration
st.set_page_config(layout="wide", page_title=None)

# Function for making spaces
def space(n,element=st): # n: number of lines
    for i in range(n):
            element.write("")

menu_data = [
    {"label": "Home", "icon": "bi bi-house"},
    {"label": "Cancer"},
    {"label": "Lung Cancer"}
]
menu_id = hc.nav_bar(
    menu_definition=menu_data, sticky_mode='sticky',
    override_theme={
        'txc_inactive': 'white',
        'menu_background': '#0178e4',
        'txc_active': '#0178e4',
        'option_active': 'white'
    }
)







# Home Menu
if menu_id == "Home":
    col1, col2, col3 = st.columns([1.2, 0.5, 1])

    col1.markdown("")
    col1.markdown("")
    col1.image("aub.png", width=300)
    col1.markdown("""<h1 style="font-size:56px;"><b>Welcome to my Streamlit page dedicated to <font color="#8B0000">Cancer</font>.</b></h1>""", unsafe_allow_html=True)

    col1.markdown("""
        <p style="font-size:24px;"><font color="#8B0000">Cancer</font> is a complex and widespread disease that affects millions of lives worldwide. It is a leading cause of illness and mortality, with various forms and impacts on individuals, families, and communities. The goal is to raise awareness, share information, and explore the latest advancements in <font color="#8B0000">cancer</font> research, prevention, and treatment. Join us on this journey to understand and combat <font color="#8B0000">cancer</font>, as we strive for a future where this devastating disease is no longer a global burden.</p>
    """, unsafe_allow_html=True)


    col1.markdown(
        """
        <style>
        .logo-container {
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    space(10,col3)
    col3.markdown("---")
    # The main image in the home page
    col3.image("cancer1.png")













# Cancer Menu
elif menu_id == "Cancer":
    def create_choropleth_map():
        fig = px.choropleth(
            df8,
            locations='Code',
            color='Deaths - Neoplasms - Sex: Both - Age: Age-standardized (Rate)',
            hover_name='Entity',
            animation_frame='Year',
            color_continuous_scale='Blues'
        )

        fig.update_layout(
            title='Cancer Death Rates Over the Years',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            )
        )


        fig.update_layout(coloraxis_showscale=False)  # Remove the color bar tick labels

        return fig



    def create_line_chart(entity, df14):
        if entity == "All":
            # Aggregate data for all entities
            aggregated_df = df14.groupby('Year').sum().reset_index()
            filtered_df = aggregated_df
        else:
            filtered_df = df14[df14['Entity'] == entity]

        # Create line chart visualization
        fig = px.line(filtered_df, x='Year',
                    y='Deaths - Neoplasms - Sex: Both - Age: All Ages (Number)',
                    title=f'Number of Deaths for {entity}',
                    labels={
                        'value': 'Deaths',
                        'variable': 'Variable',
                        'Year': 'Year'
                    })
    
        fig.update_layout(title='Number of Cancer Deaths Over the Years', showlegend=False)

        return fig



    def create_donut_chart():
        data_grouped = df3.groupby('Year').sum().reset_index()
        data_long = data_grouped.melt(id_vars="Year", value_vars=['Age 70+', 'Age 50-69', 'Age 15-49', 'Age 5-14', 'Age 5'],
                                    var_name='Age Group', value_name='Death Count')

        # Calculate the total death count for each age group
        counts = data_long.groupby('Age Group')['Death Count'].sum()

        # Define custom hex colors for each value_vars
        color_map = {
        'Age 70+': '#3366CC',
        'Age 50-69': '#3399FF',
        'Age 15-49': '#66B2FF',
        'Age 5-14': '#99CCFF',
        'Age 5': '#CCE5FF'
        }

        # Create the donut chart with custom colors
        fig = go.Figure(data=go.Pie(labels=counts.index, values=counts.values,
                                marker=dict(colors=[color_map.get(label) for label in counts.index]),
                                hole=0.6,  # Set the size of the hole in the middle (0.6 means 60% of the radius)
                                insidetextfont=dict(size=20)))

        # Update the layout to make the donut chart bigger
        fig.update_layout(
            title='Percentage of Age Groups diagnosed with cancer in 2019',
            autosize=False,
            width=800,
            height=600
        )

        return fig


    def create_bar_chart(entity, df4):
        if entity == "All":
            filtered_df = df4  # No filtering, use the entire dataframe
        else:
            filtered_df = df4[df4['Entity'] == entity]

        age_columns = filtered_df.iloc[:, 3:10]  # Select the desired age-related columns

        # Create bar chart visualization
        fig = px.bar(age_columns, x=filtered_df['Year'], y=age_columns.columns,
                    title=f'Deaths by Age for {entity}', barmode='stack',
                    color_discrete_sequence=px.colors.sequential.Blues)

        # Remove the legend
        fig.update_layout(title = 'Cancer Deaths by Age Group',showlegend=False)

        return fig
    
    # Define the Streamlit app
    def main():
        # Set the title of the app
        st.title('Cancer Dashboard')

        # Create a 2x2 grid layout
        col1, col2, col3 = st.columns([1, 2, 2])

        denmark = 334.9
        ireland = 326.6
        belgium = 322.8
        hungary = 321.6
        france = 320.1
        theme_vacc = {'bgcolor': '#f6f6f6','title_color': '#2A4657','content_color': '#0178e4','progress_color': '#0178e4','icon_color': '#0178e4'}

        # Display info card in a separate column
        with col1:
            st.subheader("Cancer Rates by Country (per 100,000)")
            hc.info_card(
                title="Denmark",
                bar_value=denmark,
                content=f"{denmark}",
                theme_override=theme_vacc
            )

            hc.info_card(
                title="Ireland",
                bar_value=ireland,
                content=f"{ireland}",
                theme_override=theme_vacc
            )
            
            hc.info_card(
                title="Belgium",
                bar_value=belgium,
                content=f"{belgium}",
                theme_override=theme_vacc
            )
            
            hc.info_card(
                title="Hungary",
                bar_value=hungary,
                content=f"{hungary}",
                theme_override=theme_vacc
            )
            hc.info_card(
                title="France",
                bar_value=france,
                content=f"{france}",
                theme_override=theme_vacc
            )
        # Display choropleth map and histogram in the second and third columns
        with col2:
            map_fig = create_choropleth_map()
            st.plotly_chart(map_fig)
            
        with col2:
            donut_fig = create_donut_chart()
            st.plotly_chart(donut_fig)
        
            
        with col3:
            entities = ['All'] + df14['Entity'].unique().tolist()
            entity = st.selectbox("Select Entity", entities, key="line_chart_entity_select")
            line_chart_fig = create_line_chart(entity, df14)
            st.plotly_chart(line_chart_fig, key="line_chart_fig")
    
        with col3:
            entities = ['All'] + df4['Entity'].unique().tolist()
            entity = st.selectbox("Select Entity", entities, key="entity_select")
            bar_chart_fig = create_bar_chart(entity, df4)
            st.plotly_chart(bar_chart_fig)

    if __name__ == '__main__':
        main()















# Lung Cancer Menu
if menu_id == "Lung Cancer":
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.subheader("Which Type of Cancer is Most Common Around the world ?")
    
    col1,col2,col3 = st.columns([3,3,3])
    
    barvalue1 = 200
    lung = 551.58
    with col1:
        theme_vacc = {'bgcolor': '#f6f6f6', 'title_color': '#2A4657', 'content_color': '#0178e4',
                    'progress_color': '#0178e4', 'icon_color': '#0178e4'}
        hc.info_card(title="Tracheal, Bronchus & Lung Cancer", bar_value=barvalue1,
                    theme_override=theme_vacc, content=f"{lung}")
        
        barvalue2 = 295.54
        recutum = 295.54
    with col2:
        theme_vacc = {'bgcolor': '#f6f6f6', 'title_color': '#2A4657', 'content_color': '#0178e4',
                    'progress_color': '#0178e4', 'icon_color': '#0178e4'}
        hc.info_card(title="Colon and Rectum Cancer", bar_value=barvalue2,
                    theme_override=theme_vacc, content=f"{recutum}")
        
        barvalue3= 247.63
        stomach = 247.63
        with col3:
            theme_vacc = {'bgcolor': '#f6f6f6', 'title_color': '#2A4657', 'content_color': '#0178e4',
                        'progress_color': '#0178e4', 'icon_color': '#0178e4'}
            hc.info_card(title="Stomach Cancer", bar_value=barvalue3,
                        theme_override=theme_vacc, content=f"{stomach}")
            
            
    # Line chart for most types of cancer and lung cancer death rates amongst men and women
    entities = ['All'] + df9['Entity'].unique().tolist()
    entity = st.selectbox("Select Entity (Cancer)", entities, key="line_chart_entity_select1")

    if entity == "All":
        # Aggregate data for all entities
        aggregated_df1 = df9.groupby('Year').sum().reset_index()
        filtered_df1 = aggregated_df1

        aggregated_df2 = df10.groupby('Year').sum().reset_index()
        filtered_df2 = aggregated_df2
    else:
        filtered_df1 = df9[df9['Entity'] == entity]
        filtered_df2 = df10[df10['Entity'] == entity]

    # Create line chart for most types of cancer
    fig1 = px.line(filtered_df1, x='Year',
                    y=['Prostate cancer', 'Breast cancer', 'Uterine cancer', 'Bladder cancer', 'Cervical cancer', 'Kidney cancer', 'Stomach cancer', 'Nasopharynx cancer', 'Testicular cancer', 'Other pharynx cancer', 'Esophageal cancer', 'Non-melanoma skin cancer', 'Pancreatic cancer', 'Tracheal, bronchus, and lung cancer', 'Lip and oral cavity cancer', 'Colon and rectum cancer', 'Gallbladder and biliary tract cancer', 'Liver cancer', 'Larynx cancer', 'Ovarian cancer', 'Thyroid cancer', 'Brain and central nervous system cancer'],
                    title=f'Number of Diagnoses for {entity} (per 100,000)',
                    labels={'value': 'Number of people diagnosed', 'variable': 'Variable', 'Year': 'Year'})

    fig1.update_layout(title='Most Common Types of Cancer', showlegend=True)

    # Create line chart for lung cancer death rates amongst men and women
    fig2 = px.line(filtered_df2, x='Year',
                    y=['Men', 'Women'],
                    title=f'Number of Lung Cancer Deaths Amongst Men & Women for {entity} (per 100,000)',
                    labels={'value': 'Number of Deaths', 'variable': 'Variable', 'Year': 'Year'})

    fig2.update_layout(title='Number of Lung Cancer Deaths Amongst Men & Women', showlegend=True)

    # Set the width and height of the charts
    chart_width = 2550
    chart_height = 600
    fig1.update_layout(width=chart_width, height=chart_height)
    
    char_width = 1200
    fig2.update_layout(width=char_width)

    # Display the charts
    st.plotly_chart(fig1, key="line_chart_fig1")

    # Line chart for cigarette sales
    entities = ['All'] + df11['Entity'].unique().tolist()

    # Create a two-column layout
    col1, col2 = st.columns([1, 1])

    # Display the chart in col2
    with col2:
        # Create an empty space for the select box
        selectbox_placeholder = st.empty()
    
        # Display the select box
        entity = selectbox_placeholder.selectbox("Select Entity (Cigarette Sales)", entities, key="line_chart_entity_select2")

        if entity == "All":
            # Aggregate data for all entities
            aggregated_df = df11.groupby('Year').sum().reset_index()
            filtered_df = aggregated_df
        else:
            filtered_df = df11[df11['Entity'] == entity]

        # Create line chart visualization
        fig3 = px.line(filtered_df, x='Year',
                        y='Sales of cigarettes per adult per day',
                        title=f'Number of Sales for Cigarettes Per Adults (Age 15+) for {entity}',
                        labels={
                            'value': 'Number of Sales',
                            'variable': 'Variable',
                            'Year': 'Year'
                        })

        fig3.update_layout(title='Number of Sales for Cigarettes Per Adults (Age 15+)', showlegend=True)
        charr_width = 1200
        fig3.update_layout(width=charr_width)
        # Display the chart
        st.plotly_chart(fig3, key="line_chart_fig3")

    # Display the first chart in col1
    with col1:
        st.plotly_chart(fig2, key="line_chart_fig2")


