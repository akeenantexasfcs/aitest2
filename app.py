#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import openai

# Set the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to process the uploaded file and display the data
def process_file(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        return df
    return None

# Function to generate a response from OpenAI
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlit App
st.title("Data Analysis Chat Interface")

# File Upload
uploaded_file = st.file_uploader("Upload your data file", type=["csv"])
df = process_file(uploaded_file)

# Chat Interface
if df is not None:
    user_input = st.text_input("Ask a question about your data")
    if st.button("Submit"):
        if user_input:
            with st.spinner('Generating response...'):
                response = generate_response(user_input)
                st.write(response)

