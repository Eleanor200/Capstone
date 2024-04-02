# chatbot.py

import streamlit as st
from streamlit_chat import message
import openai
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv


def show_chatbot_page():
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    st.title("Talk To Banky")
    st.subheader("Your Virtual Banking Assistant")
    
    model = "gpt-4"
    
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    query = st.text_input("How can I assist you with your banking today?", key="input")
    
    if 'messages' not in st.session_state:
        st.session_state['messages'] = get_initial_message()
    
    if query:
        with st.spinner("Finding the best answer for you..."):
            messages = st.session_state['messages']
            messages = update_chat(messages, "user", query)
            response = get_chatgpt_response(messages, model, domain="banking")
            messages = update_chat(messages, "assistant", response)
            st.session_state.past.append(query)
            st.session_state.generated.append(response)
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
    
