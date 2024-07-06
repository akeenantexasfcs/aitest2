#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import anthropic
import time
import random

# Set up the Anthropic client
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# Function to process the uploaded file and display the data
def process_file(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        return df
    return None

# Function to generate a response from Claude with retry mechanism
def generate_response(prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = client.completions.create(
                model="claude-3-sonnet-20240229",
                prompt=f"Human: {prompt}\n\nAssistant:",
                max_tokens_to_sample=150,
                temperature=0.7,
            )
            return response.completion.strip()
        except anthropic.RateLimitError:
            wait_time = (2 ** attempt) + random.random()
            st.warning(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return "I'm sorry, but I encountered an error while processing your request."
    
    return "I'm sorry, but I was unable to generate a response after multiple attempts."

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

