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

    col1, col2, col3 = st.columns(3)

    # Display metrics in styled cards
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="icon">🩺</div>
                <div class="label">Work-related ill-health reports</div>
                <div class="value">{1799}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="icon">📄</div>
                <div class="label">Incidents/accidents reported</div>
                <div class="value">{1283}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="icon">👩‍⚕️</div>
                <div class="label">Sickness Absence by Workforce</div>
                <div class="value">{12743}</div>
            </div>
        """, unsafe_allow_html=True)



    data = {
        'Date': pd.date_range(start='2022-01-01', periods=12, freq='M'),
        'PM2.5': [12, 15, 18, 22, 25, 30, 40, 35, 30, 25, 20, 15],  # Air quality data
        'Incidents': [50, 60, 55, 70, 65, 80, 75, 70, 60, 50, 40, 35]  # Occupational health data
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Plot a scatter plot to visualize the relationship between PM2.5 and Incidents
    scatter_fig = px.scatter(df, x='PM2.5', y='Incidents',
                            title="Relationship Between PM2.5 Levels and Occupational Health Incidents",
                            labels={'PM2.5': 'PM2.5 Levels (µg/m³)', 'Incidents': 'Reported Incidents'},
                            trendline="ols")

    # Display the scatter plot
    st.plotly_chart(scatter_fig)

    # Plot a line chart to visualize trends over time
    line_fig = px.line(df, x='Date', y=['PM2.5', 'Incidents'],
                    title="Trends in PM2.5 Levels and Occupational Health Incidents Over Time",
                    labels={'value': 'Value', 'variable': 'Metrics'})

    # Display the line chart
    st.plotly_chart(line_fig)