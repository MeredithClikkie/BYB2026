# pages/1_Flood_Timeline.py
import streamlit as st
import requests
from streamlit_timeline import timeline

# Page Configuration (Removes top padding)
st.set_page_config(layout="wide")

# THE "TOP OF PAGE" CSS
# This removes the gap and styles the vertical timeline
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
        .timeline-item { 
               border-left: 3px solid #007BFF; 
               padding-left: 20px; 
               margin-bottom: 30px; 
               position: relative; 
           }
           .timeline-item::before { 
               content: ''; 
               position: absolute; 
               left: -9px; 
               top: 0; 
               width: 15px; 
               height: 15px; 
               background-color: #007BFF; 
               border-radius: 50%; 
           }
           .date-header { color: #007BFF; font-weight: bold; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)


# Helper Function
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        return response.json()['text'] if response.status_code == 200 else "Scripture not found."
    except:
        return "Error fetching scripture."


# 3. Timeline Data Construction
# We use the approximate Masoretic text year of 2348 BC approx 1,656 years after creation popularized by Archbishop James Ussher
flood_events = [
        {
            "start_date": {"year": "2348 BC", "month": "2", "day": "10"},
            "text": {
                "headline": "Entry into the Ark",
                "text": f"<i>Genesis 7:4-10</i><br>{get_bible_text('Genesis 7:7')}"
            }
        },
        {
            "start_date": {"year": "2348 BC", "month": "2", "day": "17"},
            "text": {
                "headline": "The Flood Begins",
                "text": f"<i>Genesis 7:11</i><br>{get_bible_text('Genesis 7:11')}"
            }
        },
        {
            "start_date": {"year": "2348 BC", "month": "7", "day": "17"},
            "text": {
                "headline": "The Ark Rests",
                "text": f"<i>Genesis 8:4</i><br>{get_bible_text('Genesis 8:4')}"
            }
        },
        {
            "start_date": {"year": "2348 BC", "month": "10", "day": "1"},
            "text": {
                "headline": "Mountain Tops Visible",
                "text": f"<i>Genesis 8:5</i><br>{get_bible_text('Genesis 8:5')}"
            }
        },
        {
            "start_date": {"year": "2347 BC", "month": "2", "day": "27"},
            "text": {
                "headline": "The Earth is Dry",
                "text": f"<i>Genesis 8:14-16</i><br>{get_bible_text('Genesis 8:14')}"
            }
        }
    ]

# Option 2:
# 4. DATA LIST
# Add as many events as you like here
# flood_events = [
#    ("2nd Month, Day 17", "Genesis 7:11", "The Flood Begins"),
#    ("40 Days Later", "Genesis 7:12", "Rain Stops"),
#    ("7th Month, Day 17", "Genesis 8:4", "Ark Rests on Ararat"),
#    ("10th Month, Day 1", "Genesis 8:5", "Mountain Tops Visible"),
#    ("2nd Month, Day 27", "Genesis 8:14", "Noah Exits the Ark")
# ]

# 4. Rendering
st.title("Chronology of the Genesis Flood")

for event in flood_events:
    # Extract data from your dictionary structure
    # We use .get() to avoid errors if a key is missing
    headline = event["text"]["headline"]
    description = event["text"]["text"]

    # Format the date from the dictionary
    d = event["start_date"]
    date_str = f"Year: {d['year']}, Month: {d['month']}, Day: {d['day']}"

    with st.container():
        st.markdown(f"""
            <div class="timeline-item">
                <div class="date-header">{date_str}</div>
                <div class="ref-text"><strong>{headline}</strong></div>
            </div>
        """, unsafe_allow_html=True)
        # We don't need to call get_bible_text here because
        # it's already inside your 'description' string!
        st.info(description)

# This renders the interactive timeline at the top
timeline(flood_events, height=500)

st.divider()

# 5. Scripture Reference Section below
st.subheader("Scripture Reading")
with st.expander("Read Genesis Chapter 7"):
    st.write(get_bible_text("Genesis 7"))
with st.expander("Read Genesis Chapter 8"):
    st.write(get_bible_text("Genesis 8"))