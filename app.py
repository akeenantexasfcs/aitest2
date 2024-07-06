#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
from openai import OpenAI

# Set up the OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to process the uploaded file and display the data
def process_file(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        return df
    return None

# Function to generate a response from OpenAI
def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Make sure you have access to GPT-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

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

