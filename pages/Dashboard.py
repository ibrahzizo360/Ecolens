import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

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


co2_data = pd.read_csv('data/co2emission.csv')
rainfall_data = pd.read_csv('data/rainfall.csv')
print(rainfall_data)

# rainfall_data.fillna(0, inplace=True)

# # Melt the DataFrame to make it suitable for Plotly
# melted_data = rainfall_data.melt(id_vars=['Year', 'Month', 'Day'], var_name='City', value_name='Value')

# # Create a new column combining Year and Month for better visualization
# melted_data['Year-Month'] = pd.to_datetime(melted_data[['Year', 'Month', 'Day']])

# # Create a line chart using Plotly
# fig = px.line(
#     melted_data, 
#     x='Year-Month', 
#     y='Value', 
#     color='City',  # Differentiate lines by city
#     title='Trend of Data Across All Cities Over Time',
#     labels={
#         "Year-Month": "Date",
#         "Value": "Data Value"
#     }
# )

# # Enhance the plot with markers and a more detailed x-axis
# fig.update_traces(mode="lines+markers", marker=dict(size=5))
# fig.update_layout(
#     xaxis_title='Date',
#     yaxis_title='Data Value',
#     template='plotly_white',
#     xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
#     xaxis=dict(tickmode='linear')  # Ensure all months are displayed
# )

# # Show the plot in a Streamlit app
# st.plotly_chart(fig)

# Convert the 'Date' column to datetime format if it's not already
rainfall_data['Date'] = pd.to_datetime(rainfall_data['Date'])

# Filter data by regions using plotly's inbuilt feature
line_fig = px.line(rainfall_data, x='Date', y='Rainfall', color='Region',
                   title='Rainfall Volume Over Time by Region',
                   labels={'Rainfall': 'Rainfall (mm)', 'Date': 'Date'},
                   category_orders={"Region": sorted(rainfall_data['Region'].unique())})

# Calculate the average rainfall across all regions for each date
average_rainfall = rainfall_data.groupby('Date')['Rainfall'].mean().reset_index()

# Add the average rainfall as an additional trace to the plot
line_fig.add_scatter(x=average_rainfall['Date'], y=average_rainfall['Rainfall'],
                     mode='lines', name='Average Rainfall', line=dict(color='black', dash='dash'))

# Update the layout to include a region dropdown filter
line_fig.update_layout(
    updatemenus=[
        {
            "buttons": [
                {
                    "label": "All Regions",
                    "method": "update",
                    "args": [{"visible": [True] * (len(rainfall_data['Region'].unique()) + 1)}],
                },
            ] + [
                {
                    "label": region,
                    "method": "update",
                    "args": [{"visible": [r == region for r in rainfall_data['Region'].unique()] + [True]}],
                }
                for region in sorted(rainfall_data['Region'].unique())
            ],
            "direction": "down",
            "showactive": True,
        }
    ]
)

st.plotly_chart(line_fig)




temperature_data = pd.read_csv('data/temperature.csv')

# Ensure 'Year' is treated as a datetime column
temperature_data['Year'] = pd.to_datetime(temperature_data['Year'])

# Extract the year from the 'Year' column
temperature_data['Year'] = temperature_data['Year'].dt.year

# Aggregate the data to get the average temperatures per year
annual_avg_temperature = temperature_data.groupby('Year').agg({
    'Tn': 'mean',
    'Tx': 'mean'
}).reset_index()

# Create a Plotly figure
temp_fig = go.Figure()

# Add traces for min and max temperatures
temp_fig.add_trace(go.Scatter(x=annual_avg_temperature['Year'], y=annual_avg_temperature['Tn'],
                         mode='lines+markers',
                         name='Average Min Temperature (Tn)',
                         line=dict(color='royalblue', width=2),
                         marker=dict(size=6)))

temp_fig.add_trace(go.Scatter(x=annual_avg_temperature['Year'], y=annual_avg_temperature['Tx'],
                         mode='lines+markers',
                         name='Average Max Temperature (Tx)',
                         line=dict(color='tomato', width=2, dash='dash'),
                         marker=dict(size=6)))

# Update layout to make it more attractive
temp_fig.update_layout(
    title='Average Temperature Over Time',
    title_font_size=14,
    title_font_color='black',
    xaxis_title='Year',
    yaxis_title='Temperature (°C)',
    xaxis=dict(tickmode='linear'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey', gridwidth=1),
    legend_title='Temperature Type',
    legend_title_font_size=13,
    legend_font_size=11,
    template='simple_white',
    width=800,  # Adjust width
    height=500  # Adjust height
)


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
    st.plotly_chart(temp_fig)
