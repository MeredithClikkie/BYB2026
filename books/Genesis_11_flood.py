from streamlit_timeline import timeline

import streamlit as st

# Always make this the first Streamlit command
st.set_page_config(
    page_title="Genesis Flood Timeline",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Genesis Flood Data (Simplified JSON format)
data = {
    "events": [
        {
            "start_date": {"year": "1", "month": "2", "day": "10"},
            "text": {"headline": "God Commands Noah", "text": "Noah enters the Ark."}
        },
        {
            "start_date": {"year": "1", "month": "2", "day": "17"},
            "text": {"headline": "The Fountains Open", "text": "Rain begins for 40 days."}
        },
        {
            "start_date": {"year": "1", "month": "7", "day": "17"},
            "text": {"headline": "Ark Rests", "text": "Ark rests on the mountains of Ararat."}
        }
    ]
}

# Render the timeline at the top
timeline(data, height=400)