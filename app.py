#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import openai
import streamlit as st

st.title("ChatGPT-like clone")

# Set the API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "text-davinci-003"  # Model compatible with v0.28

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
        response = openai.Completion.create(
            engine=st.session_state["openai_model"],
            prompt="\n".join([m["content"] for m in st.session_state.messages]),
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.9,
        )
        assistant_message = response.choices[0].text.strip()
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        st.markdown(assistant_message)

