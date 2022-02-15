import requests
import json
import pandas as pd
import pickle
import streamlit as st
from streamlit_custom_slider import st_custom_slider
from streamlit_custom_slider import st_custom_select
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import datetime
import shap


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

def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

# read pickle files
with open('score_objects.pkl', 'rb') as handle:
    d, features_selected, clf, explainer = pickle.load(handle)

# explain model prediction results
def explain_model_prediction(data):
    # Calculate Shap values
    shap_values = explainer.shap_values(data)
    p = shap.force_plot(explainer.expected_value[1], shap_values[1], data)
    return p, shap_values

submit = st.button('Get predictions')

if submit:
    results = requests.post(url+endpoint, json=json_data)
    results = json.loads(results.text)
    results = pd.DataFrame([results])

    st.header('Final Result')
    prediction = results["prediction"]
    probability = results["probability"]

    st.write("Prediction: ", int(prediction))
    st.write("Probability: ", round(float(probability),3))

    #explainer force_plot
    results.drop(['prediction', 'probability'], axis=1, inplace=True)
    results = results[features_selected]
    p, shap_values = explain_model_prediction(results)
    st.subheader('Model Prediction Interpretation Plot')
    st_shap(p)

    st.subheader('Summary Plot 1')
    fig, ax = plt.subplots(nrows=1, ncols=1)
    shap.summary_plot(shap_values[1], results)
    st.pyplot(fig)

    st.subheader('Summary Plot 2')
    fig, ax = plt.subplots(nrows=1, ncols=1)
    shap.summary_plot(shap_values[1], results, plot_type='bar')
    st.pyplot(fig)