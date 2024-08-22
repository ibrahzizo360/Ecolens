import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Climate-Health Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Load data
hw_data = pd.read_excel("data/health_workforce.xlsx", header=0)
occu_health_data = pd.read_csv("data/occupational_health.csv")
ons_data = pd.read_csv("data/ons_data.csv", header=0)
hf_data = pd.read_csv("data/hf_card.csv", header=0)
co2_data = pd.read_csv('data/co2emission.csv')
rainfall_data = pd.read_csv('data/rainfall.csv')
temperature_data = pd.read_csv('data/temperature.csv')

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


# Tabs
tab1, tab2 = st.tabs(["General Climate and Health Overview", "Effects of Climate Change on Occupational Health"])

# Tab 1: Metrics Overview
with tab1:

    selected_region = st.selectbox("Select a region:", regions)

# Filter and aggregate data
    filtered_ons_data = ons_data[ons_data["region"] == selected_region].agg({
        'number_of_opd_malaria_cases': 'sum',
        'diarrhoea_diseases_all_ages': 'sum'
    })
    filtered_hw_data = hw_data[hw_data["Region"] == selected_region].agg({
        'Grand Total': 'sum'
    })
    filtered_hf_data = hf_data[hf_data["Regions"] == selected_region].agg({
        'Count of Facility': 'sum'
    })

# Display metrics
    metrics = {
        "OPD Malaria Cases": int(filtered_ons_data['number_of_opd_malaria_cases']),
        "Diarrhoea Diseases": int(filtered_ons_data['diarrhoea_diseases_all_ages']),
        "Total Health Workers": int(filtered_hw_data['Grand Total']),
        "Total Health Facilities": int(filtered_hf_data['Count of Facility'])
    }

# Define custom CSS for styling
    st.markdown("""
    <style>
        .metric-card {
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            background-color: #f0f2f6;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .metric-card .value {
            font-size: 24px;
            font-weight: bold;
        }
        .metric-card .label {
            font-size: 16px;
            color: #555;
        }
        .metric-card .icon {
            font-size: 30px;
            color: #007bff;
            margin-right: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    # Create four columns
    col1, col2, col3, col4 = st.columns(4)

    # Display metrics in styled cards
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="icon">🩺</div>
                <div class="label">OPD Malaria Cases</div>
                <div class="value">{metrics["OPD Malaria Cases"]}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="icon">💧</div>
                <div class="label">Diarrhoea Diseases</div>
                <div class="value">{metrics["Diarrhoea Diseases"]}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="icon">👩‍⚕️</div>
                <div class="label">Total Health Workers</div>
                <div class="value">{metrics["Total Health Workers"]}</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="icon">🏥</div>
                <div class="label">Total Health Facilities</div>
                <div class="value">{metrics["Total Health Facilities"]}</div>
            </div>
        """, unsafe_allow_html=True)



    # Convert 'Date' column to datetime format
    rainfall_data['Date'] = pd.to_datetime(rainfall_data['Date'])

    # Create Plotly figure for rainfall data
    line_fig = px.line(rainfall_data, x='Date', y='Rainfall', color='Region',
                       title='Rainfall Volume Over Time by Region',
                       labels={'Rainfall': 'Rainfall (mm)', 'Date': 'Date'},
                       category_orders={"Region": sorted(rainfall_data['Region'].unique())})

    # Calculate average rainfall
    average_rainfall = rainfall_data.groupby('Date')['Rainfall'].mean().reset_index()
    line_fig.add_scatter(x=average_rainfall['Date'], y=average_rainfall['Rainfall'],
                         mode='lines', name='Average Rainfall', line=dict(color='black', dash='dash'))

    # Update layout with dropdown filter
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

    # Prepare temperature data
    temperature_data['Year'] = pd.to_datetime(temperature_data['Year']).dt.year
    annual_avg_temperature = temperature_data.groupby('Year').agg({
        'Tn': 'mean',
        'Tx': 'mean'
    }).reset_index()

    # Create Plotly figure for temperature data
    temp_fig = go.Figure()
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

    # Update layout for temperature figure
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

    # Create Plotly figure for CO2 data
    co2_data['Year'] = pd.to_datetime(co2_data['Year'], format='%Y')
    co2_fig = px.line(co2_data, x='Year', y='CO2 emission', title='CO2 Emissions Over Time')

    # Create columns for visualizations
    col1, col2 = st.columns([1, 2])  # 40% and 60% width ratio

    # Display the first plot in the first column
    with col1:
        st.plotly_chart(co2_fig)

    # Display the second plot in the second column
    with col2:
        st.plotly_chart(temp_fig)

# Tab 2: Visualizations
with tab2:
    st.header("Occupational Health Overview and Climate Impact")

    # 1. Occupational Health Overview by Region
    st.subheader("Occupational Health Metrics by Region")

    # Filter data by selected region
    region_data = occu_health_data[occu_health_data['Region'] == selected_region]

    # Bar chart for work-related ill-health reports
    fig_ill_health = px.bar(region_data, x='District', y='Number of work-related ill-health reports',
                            title="Work-related Ill-health Reports by District",
                            labels={'Number of work-related ill-health reports': 'Ill-health Reports'},
                            color='Facility_ownership')
    st.plotly_chart(fig_ill_health)

    # Stacked bar chart for injured persons (Male and Female)
    fig_injured = go.Figure(data=[
        go.Bar(name='Female', x=region_data['District'], y=region_data['Number of injured persons (Female)']),
        go.Bar(name='Male', x=region_data['District'], y=region_data['Number of injured persons (Male)'])
    ])
    fig_injured.update_layout(barmode='stack', title="Injured Persons by District and Gender")
    st.plotly_chart(fig_injured)

    # 2. Correlation Analysis
    st.subheader("Correlation Between Occupational Health and Climate Factors")

    # Merge data with climate data on a common period or year
    # Convert 'Period' to a common format if needed (e.g., year)
    region_data['Period'] = pd.to_datetime(region_data['Period']).dt.year
    co2_data['Year'] = pd.to_datetime(co2_data['Year'], format='%Y').dt.year
    temperature_data['Year'] = pd.to_datetime(temperature_data['Year']).dt.year

    # Filter or aggregate occupational health data to match the climate data by year
    aggregated_region_data = region_data.groupby('Period').agg({
        'Number of incidents/accidents reported': 'sum'
    }).reset_index()

    # Merge the aggregated region data with the CO2 data
    merged_data_co2 = pd.merge(aggregated_region_data, co2_data, left_on='Period', right_on='Year', how='inner')

    # Merge the aggregated region data with the temperature data
    merged_data_temp = pd.merge(aggregated_region_data, temperature_data, left_on='Period', right_on='Year', how='inner')

    # Scatter plots for correlation analysis
    st.write("Scatter plot of incidents/accidents vs. CO2 emissions")
    fig_corr_co2 = px.scatter(merged_data_co2, x='Number of incidents/accidents reported',
                            y='CO2 emission',
                            title="Incidents vs CO2 Emissions",
                            labels={'Number of incidents/accidents reported': 'Incidents/Accidents',
                                    'CO2 emission': 'CO2 Emissions (tons)'})
    st.plotly_chart(fig_corr_co2)

    st.write("Scatter plot of incidents/accidents vs. Average Temperature")
    fig_corr_temp = px.scatter(merged_data_temp, x='Number of incidents/accidents reported',
                            y='Tx',
                            title="Incidents vs Average Temperature",
                            labels={'Number of incidents/accidents reported': 'Incidents/Accidents',
                                    'Tx': 'Average Temperature (°C)'})
    st.plotly_chart(fig_corr_temp)

    # 3. Trend Analysis Over Time
    st.subheader("Trends in Occupational Health and Climate Data")

    # Line chart for trends in health data over time
    fig_trend_health = px.line(region_data, x='Period', y='Number of work-related ill-health reports',
                            title="Trends in Work-related Ill-health Reports Over Time",
                            labels={'Number of work-related ill-health reports': 'Ill-health Reports'})
    st.plotly_chart(fig_trend_health)

    # Overlay with climate data trends
    fig_trend_co2 = px.line(co2_data, x='Year', y='CO2 emission', title="CO2 Emissions Over Time")
    fig_trend_rainfall = px.line(rainfall_data, x='Date', y='Rainfall', title="Rainfall Over Time")
    fig_trend_temp = px.line(temperature_data, x='Year', y='Tx', title="Average Temperature Over Time")

    # Display the climate trends
    st.plotly_chart(fig_trend_co2)
    st.plotly_chart(fig_trend_rainfall)
    st.plotly_chart(fig_trend_temp)
