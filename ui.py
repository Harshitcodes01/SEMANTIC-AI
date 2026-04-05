import streamlit as st
from workflow import run_pipeline


st.title("PRANA-G AI Orchestrator")

user_input = st.text_input("Enter your prompt")

if st.button("Generate Spec"):
    result = run_pipeline(user_input)
    st.json(result)