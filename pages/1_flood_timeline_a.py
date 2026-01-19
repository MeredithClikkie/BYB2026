# pages/1_Flood_Timeline.py
import streamlit as st
import requests
from streamlit_timeline import timeline

def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        return response.json()['text'] if response.status_code == 200 else None
    except Exception as e:
        return None

st.set_page_config(layout="wide") # Important for a top-of-page look

# 1. Define the variables first
flood_start_text = get_bible_text("Genesis 7:11")
ark_rests_text = get_bible_text("Genesis 8:4")
mountain_tops_text = get_bible_text("Genesis 8:5")
earth_dry_text = get_bible_text("Genesis 8:14")

# # Timeline Data Structure
flood_data = {
    "events": [
        {
            "start_date": {"year": "600", "month": "2", "day": "17"},
            "text": {
                "headline": "The Flood Begins",
                "text": flood_start_text or "The fountains of the great deep were broken up."
            }
        },
        {
            "start_date": {"year": "600", "month": "7", "day": "17"},
            "text": {
                "headline": "The Ark Rests",
                "text": ark_rests_text or "The ark rested upon the mountains of Ararat."
            }
        }
] }
# --- Page Layout ---
st.set_page_config(layout="wide")

# Fetching specific data for the timeline
# You can use your function to populate the 'text' fields below
flood_start_text = get_bible_text("Genesis 7:11")
ark_rests_text = get_bible_text("Genesis 8:4")

# 3. Render the timeline at the top
st.title("The Genesis Flood Chronology")
timeline(flood_data, height=500)