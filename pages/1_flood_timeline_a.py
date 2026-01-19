# pages/1_Flood_Timeline.py
import streamlit as st
import requests
from streamlit_timeline import timeline


# 1. Page Configuration (Must be the very first Streamlit command)
st.set_page_config(page_title="Genesis Flood Timeline", layout="wide")

# 2. CSS for Top-of-Page Positioning and Timeline Styling
st.markdown("""
    <style>
           .block-container { padding-top: 1rem; }
           .timeline-item { 
               border-left: 3px solid #704214; 
               padding-left: 20px; 
               margin-bottom: 30px; 
               position: relative; 
           }
           .timeline-item::before { 
               content: ''; 
               position: absolute; 
               left: -10px; 
               top: 0; 
               width: 16px; 
               height: 16px; 
               background-color: #704214; 
               border-radius: 50%; 
           }
           .date-header { color: #704214; font-weight: bold; font-size: 1.1rem; }
           .headline { font-size: 1.5rem; font-weight: bold; margin-top: -5px; }
    </style>
    """, unsafe_allow_html=True)


# 3. Cached Bible API Function
@st.cache_data
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['text'].strip()
        return "Scripture text not found."
    except Exception:
        return "Connection error."


# 4. The Data (Structured as Dictionaries)
flood_events = [
    {
        "date_label": "Year 600, Month 2, Day 10",
        "headline": "Entry into the Ark",
        "ref": "Genesis 7:7",
        "note": "Noah and his family enter the ark seven days before the rain begins."
    },
    {
        "date_label": "Year 600, Month 2, Day 17",
        "headline": "The Flood Begins",
        "ref": "Genesis 7:11",
        "note": "The fountains of the great deep burst forth and the windows of heaven opened."
    },
    {
        "date_label": "Year 600, Month 7, Day 17",
        "headline": "The Ark Rests",
        "ref": "Genesis 8:4",
        "note": "Exactly 150 days after the flood began, the ark rests on Ararat."
    },
    {
        "date_label": "Year 600, Month 10, Day 1",
        "headline": "Mountain Tops Visible",
        "ref": "Genesis 8:5",
        "note": "The waters continued to recede until the peaks of the mountains were seen."
    },
    {
        "date_label": "Year 601, Month 2, Day 27",
        "headline": "The Earth is Dry",
        "ref": "Genesis 8:14",
        "note": "Noah and his family exit the ark. The total duration was approximately 371 days."
    }
]

# 5. Rendering the Page
st.title("Chronology of the Genesis Flood")
st.write("A timeline based on the account in Genesis 7 and 8.")

# The Loop (Correctly accessing the Dictionary keys)
for event in flood_events:
    with st.container():
        # Display the custom styled "dot and line" header
        st.markdown(f"""
            <div class="timeline-item">
                <div class="date-header">{event['date_label']}</div>
                <div class="headline">{event['headline']}</div>
            </div>
        """, unsafe_allow_html=True)

        # Fetch the Bible text dynamically based on the 'ref' key
        bible_text = get_bible_text(event['ref'])

        # Display the text in a nice box
        st.info(f"**{event['ref']}**: {bible_text}")
        st.caption(f"Note: {event['note']}")
        st.write("")  # Add some spacing