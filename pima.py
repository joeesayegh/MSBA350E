import streamlit as st
import plotly.express as px
import pandas as pd
import hydralit_components as hc

df = pd.read_csv("diabetes.csv")

st.set_page_config(layout="wide", page_title=None)

# Creating Navigation bar
menu_data = [{"label": "Home", 'icon': "bi bi-house"}, {'label': 'Dashboard'}]
menu_id = hc.nav_bar(menu_definition=menu_data, sticky_mode='sticky',
                     override_theme={'txc_inactive': 'white',
                                     'menu_background': '#0178e4',
                                     'txc_active': '#0178e4',
                                     'option_active': 'white'})

if menu_id == "Home":
    st.header("Welcome to Healthcare Analytics Individual assignment")
    st.subheader("Global Overview")
    st.text("Add your content here")

else:
    # Create Plotly figures or graphs
    def create_scatter_plot():
        # Create scatter plot visualization
        fig = px.scatter(df, x='Glucose', y='BloodPressure', color='Outcome')
        return fig

    def create_histogram():
        # Create histogram visualization
        fig = px.histogram(df, x='BMI')
        return fig

    def create_bar_chart():
        # Create bar chart visualization
        fig = px.bar(df, x='Age', y='Outcome')
        return fig

    def create_line_chart():
        # Filter the dataset for entries with diabetes (Outcome = 1)
        df_diabetes = df[df['Outcome'] == 1]

        # Create a line chart for ages with diabetes
        fig = px.line(df_diabetes, x='Outcome', y='Age', title='Trend of Ages with Diabetes')
        fig.update_traces(mode='markers+lines')  # Show markers at each data point
        fig.update_layout(xaxis_title='Diabetes', yaxis_title='Age')
        return fig

    # Define the Streamlit app
    def main():
        # Set the title of the app
        st.title('Diabetes Dashboard')

        # Add description or explanation if needed
        st.markdown("This dashboard visualizes the diabetes dataset.")

        # Create a 2x2 grid layout
        col1, col2, col3 = st.columns([1, 2, 2])

        # Calculate the count of females diagnosed with diabetes
        female_count0 = 500
        female_count1 = 268

        theme_vacc = {'bgcolor':'#cfe2f3','content_color':'navy','progress_color':'navy'}

        # Display info card in a separate column
        with col1:
            st.subheader("The data")
            hc.info_card(
                title="Diabetic",
                bar_value=female_count1,
                content=f"{female_count1}",
                theme_override=theme_vacc
            )

            hc.info_card(
                title="NonDiabetic",
                bar_value=female_count0,
                content=f"{female_count0}",
                theme_override=theme_vacc
            )

        # Display scatter plot and histogram in the second column
        with col2:
            st.subheader("Scatter Plot")
            scatter_fig = create_scatter_plot()
            st.plotly_chart(scatter_fig)

            st.subheader("Histogram")
            hist_fig = create_histogram()
            st.plotly_chart(hist_fig)

        # Display bar chart and line chart in the third column
        with col3:
            st.subheader("Bar Chart")
            bar_fig = create_bar_chart()
            st.plotly_chart(bar_fig)

            st.subheader("Line Chart")
            line_fig = create_line_chart()
            st.plotly_chart(line_fig)

    if __name__ == '__main__':
        main()