import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Climate-Health Dashboard",
    layout="wide",
)

files = {
    "CO2 Emissions": "data/co2.csv",
    "Health Workforce": "data/health_workforce.xlsx",
    "Malnutrition": "data/malnutrition.xls",
    "Occupational Health": "data/occupational_health.xls",
    "ONS": "data/ons.xlsx",
    "Population": "data/population.xlsx",
    "Rainfall": "data/rainfall.xlsx",
    "Temperature": "data/temperature.xls"
}

# Load and create DataFrames
dfs = {}
for name, file_path in files.items():
    try:
        # Determine file type by extension and load accordingly
        if file_path.endswith('.csv'):
            dfs[name] = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            dfs[name] = pd.read_excel(file_path)
        elif file_path.endswith('.xls'):
            dfs[name] = pd.read_excel(file_path)
        else:
            st.error(f"Unsupported file type for {file_path}")
            continue
        st.write(f"### {name}")
        st.dataframe(dfs[name])
    except Exception as e:
        st.error(f"Error loading {name}: {str(e)}")

# Display DataFrames in cards
st.markdown("<h2 style='text-align: center;'>Data Cards</h2>", unsafe_allow_html=True)