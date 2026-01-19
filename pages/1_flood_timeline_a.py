# pages/1_Flood_Timeline.py
import streamlit as st
import requests
from streamlit_timeline import timeline

# 1. Helper Function
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        return response.json()['text'] if response.status_code == 200 else "Scripture not found."
    except Exception:
        return "Error fetching scripture."

# 2. Page Configuration (Removes top padding)
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. Timeline Data Construction
# We use a placeholder 'year' (600) to represent Noah's age
flood_events = {
    "events": [
        {
            "start_date": {"year": "600", "month": "2", "day": "10"},
            "text": {
                "headline": "Entry into the Ark",
                "text": f"<i>Genesis 7:4-10</i><br>{get_bible_text('Genesis 7:7')}"
            }
        },
        {
            "start_date": {"year": "600", "month": "2", "day": "17"},
            "text": {
                "headline": "The Flood Begins",
                "text": f"<i>Genesis 7:11</i><br>{get_bible_text('Genesis 7:11')}"
            }
        },
        {
            "start_date": {"year": "600", "month": "7", "day": "17"},
            "text": {
                "headline": "The Ark Rests",
                "text": f"<i>Genesis 8:4</i><br>{get_bible_text('Genesis 8:4')}"
            }
        },
        {
            "start_date": {"year": "600", "month": "10", "day": "1"},
            "text": {
                "headline": "Mountain Tops Visible",
                "text": f"<i>Genesis 8:5</i><br>{get_bible_text('Genesis 8:5')}"
            }
        },
        {
            "start_date": {"year": "601", "month": "2", "day": "27"},
            "text": {
                "headline": "The Earth is Dry",
                "text": f"<i>Genesis 8:14-16</i><br>{get_bible_text('Genesis 8:14')}"
            }
        }
    ]
}

# 4. Rendering
st.title("Chronology of the Genesis Flood")

# This renders the interactive timeline at the top
timeline(flood_events, height=500)

st.divider()

# 5. Scripture Reference Section below
st.subheader("Scripture Reading")
with st.expander("Read Genesis Chapter 7"):
    st.write(get_bible_text("Genesis 7"))
with st.expander("Read Genesis Chapter 8"):
    st.write(get_bible_text("Genesis 8"))