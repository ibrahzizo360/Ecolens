import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Climate-Health Dashboard",
    layout="wide",
)

climate_data = pd.read_excel('data/temperature.xls')
df = pd.DataFrame(climate_data)

# Display DataFrame
st.dataframe(df)