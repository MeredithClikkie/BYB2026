# books/genesis.py
import streamlit as st
import requests
from streamlit_timeline import timeline

# Always make this the first Streamlit command
st.set_page_config(
    page_title="Genesis Flood Timeline",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 3. Cached Bible API Function

def get_data():
    """Provides data to the superior script."""
    return [
        {"Event": "Creation/Fall", "Date": -4000},
        {"Event": "The Flood", "Date": -2400},
        {"Event": "Call of Abraham", "Date": -2091},
        {"Event": "Joseph in Egypt", "Date": -1898},
        {"Event": "Jacob Moves to Egypt", "Date": -1876}
    ]

def get_specific_patterns():
    """Patterns unique to Genesis."""
    return [
        {"label": "GPE", "pattern": [{"LOWER": "eden"}]},
        {"label": "GPE", "pattern": [{"LOWER": "ararat"}]}
    ]



