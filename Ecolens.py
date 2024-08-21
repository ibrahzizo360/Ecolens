import pandas as pd
import openai
import os
import streamlit as st
#import streamlit_nested_layout
from classes import get_primer,format_question,run_request,run_explanation_request
import warnings
from dotenv import load_dotenv

load_dotenv()  
warnings.filterwarnings("ignore")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_icon="old-logo.png",layout="wide",page_title="Ecolens")


st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            Ecolens</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>Visualizing the impact of climate change on health through natural language insights.</h2>", unsafe_allow_html=True)

st.sidebar.markdown('</a> Developed by Team BroCode <a style="text-align: center;padding-top: 0rem;" href="mailto: ibrahziz10@gmail.com">:email:', unsafe_allow_html=True)

# List to hold datasets
if "datasets" not in st.session_state:
    datasets = {}
    # Preload datasets
    datasets["Movies"] = pd.read_csv("movies.csv")
    datasets["Housing"] =pd.read_csv("housing.csv")
    datasets["Cars"] =pd.read_csv("cars.csv")
    datasets["Colleges"] =pd.read_csv("colleges.csv")
    datasets["Customers & Products"] =pd.read_csv("customers_and_products_contacts.csv")
    datasets["Department Store"] =pd.read_csv("department_store.csv")
    datasets["Energy Production"] =pd.read_csv("energy_production.csv")
    st.session_state["datasets"] = datasets
else:
    # use the list already loaded
    datasets = st.session_state["datasets"]

groq_key=os.getenv('groq_key')
print('groq_key is  ', groq_key)

with st.sidebar:
    # First we want to choose the dataset, but we will fill it with choices once we've loaded one
    dataset_container = st.empty()

    # Add facility to upload a dataset
    try:
        uploaded_file = st.file_uploader(":computer: Load a CSV file:", type="csv")
        index_no=0
        if uploaded_file:
            # Read in the data, add it to the list of available datasets. Give it a nice name.
            file_name = uploaded_file.name[:-4].capitalize()
            datasets[file_name] = pd.read_csv(uploaded_file)
            # We want to default the radio button to the newly added dataset
            index_no = len(datasets)-1
    except Exception as e:
        st.error("File failed to load. Please select a valid CSV file.")
        print("File failed to load.\n" + str(e))
    # Radio buttons for dataset choice
    chosen_dataset = dataset_container.radio(":bar_chart: Choose your data:",datasets.keys(),index=index_no)#,horizontal=True,)
 
 # Text area for query
st.markdown(
    """
    <style>
    .stTextArea label p {
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
question = st.text_area(":eyes: What would you like to visualise?",height=10)
go_btn = st.button("Go...")

# Make a list of the models which have been selected
selected_models = ["gpt-3.5-turbo-instruct"]
model_count = 1

# Execute chatbot query
if go_btn and model_count > 0:
    api_keys_entered = True
    # Check API keys are entered.
    if api_keys_entered:
        # Place for plots depending on how many models
        plots = st.columns(model_count)
        # Get the primer for this dataset
        primer1,primer2 = get_primer(datasets[chosen_dataset],'datasets["'+ chosen_dataset + '"]') 
        # Create model, run the request and print the results
        for plot_num, model_type in enumerate(selected_models):
            with plots[plot_num]:
                try:
                    # Format the question 
                    question_to_ask = format_question(primer1, primer2, question, model_type)   
                    # Run the question
                    answer=""
                    answer = run_request(question_to_ask, key=groq_key)
                    # the answer is the completed Python script so add to the beginning of the script to it.
                    answer = primer2 + answer
                    print(answer)
                    plot_area = st.empty()
                    plot_area.pyplot(exec(answer))    
                    
                    # AI-Generated Explanation
                    explanation_query = f"Explain the findings and insights from the following visualization: {question_to_ask}"
                    explanation = run_explanation_request(explanation_query, key=groq_key)
                    # st.markdown("###Insights")
                    st.write(explanation)       
                except Exception as e:
                    print(e)
                    if type(e) == openai.error.APIError:
                        st.error("OpenAI API Error. Please try again a short time later. (" + str(e) + ")")       
                    else:
                        st.error("Unfortunately the code generated from the model contained errors and was unable to execute.")

# Display the datasets in a list of tabs
# Create the tabs
tab_list = st.tabs(datasets.keys())

# Load up each tab with a dataset
for dataset_num, tab in enumerate(tab_list):
    with tab:
        # Can't get the name of the tab! Can't index key list. So convert to list and index
        dataset_name = list(datasets.keys())[dataset_num]
        st.subheader(dataset_name)
        st.dataframe(datasets[dataset_name],hide_index=True)

# Hide menu and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
