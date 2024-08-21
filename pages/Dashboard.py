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

data = {
    "CO2 Emissions": pd.DataFrame({
        "Country": ["USA", "China", "India", "Russia"],
        "Emissions": [5000, 9000, 2000, 1500]
    }),
    "Health Workforce": pd.DataFrame({
        "Country": ["USA", "UK", "Germany", "France"],
        "Doctors": [300000, 15000, 12000, 10000]
    }),
    "Malnutrition": pd.DataFrame({
        "Country": ["Nigeria", "India", "Pakistan", "Bangladesh"],
        "Percentage": [20, 25, 22, 18]
    }),
    "Occupational Health": pd.DataFrame({
        "Country": ["USA", "China", "Germany", "Japan"],
        "Injuries": [500, 800, 300, 200]
    }),
    "Population": pd.DataFrame({
        "Country": ["USA", "China", "India", "Brazil"],
        "Population": [331, 1441, 1393, 213]
    }),
}

cols = st.columns(5)
metric_style = """
<div style='background-color: #f5f5f5; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);'>
    <h4 style='font-size: 1.25em; color: #4a4a4a;'>{label}</h4>
    <p style='font-size: 2em; color: #0073e6; margin: 10px 0;'>{value}</p>
</div>
"""
# Display each DataFrame's metric in a styled card
for i, (name, df) in enumerate(data.items()):
    if i < 5:  # Limit to the first 4 DataFrames
        with cols[i]:
            if "Emissions" in df.columns:
                total = df["Emissions"].sum()
                st.markdown(metric_style.format(label=name, value=f"{total} tons"), unsafe_allow_html=True)
            elif "Doctors" in df.columns:
                total = df["Doctors"].sum()
                st.markdown(metric_style.format(label=name, value=f"{total} doctors"), unsafe_allow_html=True)
            elif "Percentage" in df.columns:
                average = df["Percentage"].mean()
                st.markdown(metric_style.format(label=name, value=f"{average}%"), unsafe_allow_html=True)
            elif "Injuries" in df.columns:
                total = df["Injuries"].sum()
                st.markdown(metric_style.format(label=name, value=f"{total} injuries"), unsafe_allow_html=True)
            elif "Population" in df.columns:
                total = df["Population"].sum()
                st.markdown(metric_style.format(label=name, value=f"{total} million"), unsafe_allow_html=True)


df = px.data.gapminder().query("continent=='Oceania'")
fig = px.line(df, x="year", y="lifeExp", color='country')

# Data for the second plot
data_canada = px.data.gapminder().query("country == 'Canada'")
bar_fig = px.bar(data_canada, x='year', y='pop')

# Create two columns
col1, col2 = st.columns(2)

# Display the first plot in the first column
with col1:
    st.plotly_chart(fig)

# Display the second plot in the second column
with col2:
    st.plotly_chart(bar_fig)
