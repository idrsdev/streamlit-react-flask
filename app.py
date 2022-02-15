import requests
import json
import pandas as pd
import streamlit as st
from streamlit_custom_slider import st_custom_slider
from streamlit_custom_slider import st_custom_select

st.title('Python Real Time Scoring API + Model Explainer')

# Python API endpoint
url = 'http://pythonapi:5000'
endpoint = '/api/'

# description and instructions
st.write('''A real time scoring API for Python model.''')

input_features = {}
#Age
input_features["age"] = st_custom_slider('Age', 18, 95, 50, key="age")
# Education
input_features["education"] = st_custom_select('Education Qualification', ['tertiary', 'secondary', 'unknown', 'primary'],default='tertiary',key='education')
# Balance
input_features["balance"] = st_custom_slider('Current balance', -10000, 150000, 0, key="balance")
# Housing
input_features["housing"] = st_custom_select('Do you own a home?', ['yes', 'no'],default='yes',key='Housing')
# Loan
input_features["loan"] = st_custom_select('Do you have a loan?', ['yes', 'no'],default='yes',key='Loan')
# contact
input_features["contact"] = st_custom_select('Best way to contact you', ['cellular', 'telephone', 'unknown'],default='cellular',key='contact')
# Date
date = st.date_input("Today's Date")
input_features["day"] = date.day
input_features["month"] = date.strftime("%b").lower()
# Duration
input_features["duration"] = st_custom_slider('Duration', 0, 5000,50,key='duration')
input_features["campaign"] = st_custom_slider('Campaign', 1, 63,50,key='campaign')
input_features["pdays"] = st_custom_slider('pdays', -1, 871,50,key='pdays')
input_features["previous"] = st_custom_slider('previous', 0, 275,50,key='previous')
input_features["poutcome"] = st_custom_select('poutcome', ['success', 'failure', 'other', 'unknown'],default='success',key='poutcome')

def user_input_features():
    return [input_features]

json_data = user_input_features()

submit = st.button('Get predictions')
if submit:
    # Input Data , Format=Json
    results = requests.post(url+endpoint, json=json_data)
    # Converting Output to Json Format
    results = json.loads(results.text) 
    results = pd.DataFrame([results])
    #It automaticaly detects its a pandas dataframe and displays it
    # st.write(results) # Can also be passed to Custom Components
    results