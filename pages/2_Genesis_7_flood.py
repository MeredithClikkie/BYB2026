import streamlit as st
import requests
import json
from streamlit_timeline import timeline

# 1. PAGE SETUP
st.set_page_config(layout="wide")

# This CSS keeps the timeline at the very top
st.markdown("<style>.block-container {padding-top: 0rem;}</style>", unsafe_allow_html=True)

# 2. BIBLE API (Cached for speed)
@st.cache_data
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        r = requests.get(url)
        return r.json()['text'] if r.status_code == 200 else "Text not found."
    except:
        return "Connection Error"

# 3. CONSTRUCT THE DATA CAREFULLY
# We build this inside a function to ensure it's clean before passing to the component
def get_flood_data():
    return {
        "events": [
            {
                "start_date": {"year": -2348, "month": "2", "day": "10"},
                "display_date": "2348 BC month 2 day 10",
                "text": {
                    "headline": "Entry into the Ark",
                    "text": f"Genesis 7:7<br><br>{get_bible_text('Genesis 7:7')}"
                }
            },
            {
                "start_date": {"year": -2348, "month": "2", "day": "17"},
                "display_date": "2348 BC month 2 day 17",
                "text": {
                    "headline": "The Flood Begins",
                    "text": f"Genesis 7:11<br><br>{get_bible_text('Genesis 7:11')}"
                }
            },
            {
                "start_date": {"year": -2348, "month": "7", "day": "17"},
                "display_date": "2348 BC month 7 day 17",
                "text": {
                    "headline": "The Ark Rests",
                    "text": f"Genesis 8:4<br><br>{get_bible_text('Genesis 8:4')}"
                }
            },
            {
                "start_date": {"year": -2348, "month": "10", "day": "1"},
                "display_date": "2348 BC month 10 day 1",
                "text": {
                    "headline": "Mountain Tops Visible",
                    "text": f"Genesis 8:5<br><br>{get_bible_text('Genesis 8:5')}"
                }
            },
            {
                "start_date": {"year": -2347, "month": "2", "day": "27"},
                "display_date": "2347 BC month 2 day 27",
                "text": {
                    "headline": "Noah Leaves the Ark",
                    "text": f"Genesis 8:14<br><br>{get_bible_text('Genesis 8:14')}"
                }
            }
        ]
    }

# 4. RENDER
st.title("Genesis Flood Timeline")

data = get_flood_data()

# Safety Check: If data exists, show timeline.
# We use json.dumps to ensure the component receives a clean string.
try:
    timeline(data, height=500)
except Exception as e:
    st.error("The timeline component failed to load. Please check your internet connection (needed for the JS libraries).")
    st.write(e)