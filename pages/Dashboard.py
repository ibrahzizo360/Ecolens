import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Climate-Health Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

cols = st.columns(2)
metric_style = """
<div style='background-color: #f5f5f5; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);'>
    <h4 style='font-size: 1.25em; color: #4a4a4a;'>{label}</h4>
    <p style='font-size: 2em; color: #0073e6; margin: 10px 0;'>{value}</p>
</div>
"""

hw_data = pd.read_excel("data/health_workforce.xlsx", header=0)
ons_data = pd.read_csv("data/ons_data.csv", header=0)
hf_data = pd.read_csv("data/hf_card.csv", header=0)

# Replace any NA values with 0
ons_data.fillna(0, inplace=True)
hw_data.fillna(0, inplace=True)

print(hf_data)

# List of regions
regions = [
    'Ahafo', 'Ashanti', 'Bono', 'Bono East', 'Central', 'Eastern', 
    'Greater Accra', 'North East', 'Northern', 'Oti', 'Savannah', 
    'Upper East', 'Upper West', 'Volta', 'Western', 'Western North'
]

# Streamlit selectbox for region selection
selected_region = st.selectbox("Select a region:", regions)

# Filter the ons_data DataFrame for the selected region and aggregate the values
filtered_ons_data = ons_data[ons_data["region"] == selected_region].agg({
    'number_of_opd_malaria_cases': 'sum',
    'diarrhoea_diseases_all_ages': 'sum'
})

# Filter the hw_data DataFrame for the selected region
filtered_hw_data = hw_data[hw_data["Region"] == selected_region].agg({
    'Grand Total': 'sum'
})

# Filter the hw_data DataFrame for the selected region
filtered_hf_data = hf_data[hf_data["Regions"] == selected_region].agg({
    'Count of Facility': 'sum'
})

# Display the metrics in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="OPD Malaria Cases", value=int(filtered_ons_data['number_of_opd_malaria_cases']))

with col2:
    st.metric(label="Diarrhoea Diseases", value=int(filtered_ons_data['diarrhoea_diseases_all_ages']))

with col3:
    st.metric(label="Total Health Workers", value=int(filtered_hw_data['Grand Total']))

with col4:
    st.metric(label="Total Health Facilities", value=int(filtered_hf_data['Count of Facility']))



df = px.data.gapminder().query("continent=='Oceania'")
fig = px.line(df, x="year", y="lifeExp", color='country')

# Data for the second plot
data_canada = px.data.gapminder().query("country == 'Canada'")
bar_fig = px.bar(data_canada, x='year', y='pop')

co2_data = pd.read_csv('data/co2emission.csv')
rainfall_data = pd.read_csv('data/co2emission.csv')

# Ensure that the time column is in datetime format
co2_data['Year'] = pd.to_datetime(co2_data['Year'], format='%Y')

# Plot a time series using Plotly
fig = px.line(co2_data, x='Year', y='CO2 emission', title='CO2 Emissions Over Time')


# Create two columns
col1, col2 = st.columns(2)

# Display the first plot in the first column
with col1:
    st.plotly_chart(fig)

# Display the second plot in the second column
with col2:
    st.plotly_chart(bar_fig)
