#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import openai

# Function to initialize OpenAI API key
def init_openai():
    openai.api_key = "sk-proj-bvQPXeZci5ho6xHm13HaT3BlbkFJB9wxNeE3Sqxj0XmLHtOB"

# Function to process the uploaded file and display the data
def process_file(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        return df
    return None

# Function to generate a response from OpenAI
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # You can also use "gpt-3.5-turbo" if you don't have access to GPT-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# Streamlit App
st.title("Data Analysis Chat Interface")

# Initialize OpenAI API key
init_openai()

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

                
                
                

