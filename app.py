#!/usr/bin/env python
# coding: utf-8

# In[12]:


import subprocess
import sys

# Upgrade openai library
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "openai"])

import openai
import streamlit as st

st.title("ChatGPT-like clone")

# Set the API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )
        st.session_state.messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        st.markdown(response['choices'][0]['message']['content'])


# In[ ]:




