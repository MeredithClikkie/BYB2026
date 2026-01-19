import streamlit as st
import requests
from streamlit_timeline import timeline

# 1. PAGE SETUP (Must be first)
st.set_page_config(page_title="Genesis Flood Timeline", layout="wide")

# 2. CSS FOR TOP-OF-PAGE AND STYLING
st.markdown("""
    <style>
           /* Remove gap at the top */
           .block-container { padding-top: 0rem; }

           /* Vertical Timeline Styling */
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
           .headline-style { font-size: 1.5rem; font-weight: bold; margin-top: -5px; }
    </style>
    """, unsafe_allow_html=True)


# 3. CACHED BIBLE API FUNCTION
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


# 4. DATA PREPARATION
# This list powers both the horizontal box and the vertical list
raw_data = [
    {
        "year": -2348, "month": 2, "day": 10,
        "label": "2348 BC - Month 2, Day 10",
        "headline": "Entry into the Ark",
        "ref": "Genesis 7:7",
        "note": "Noah and his family enter the ark seven days before the rain begins."
    },
    {
        "year": -2348, "month": 2, "day": 17,
        "label": "2348 BC - Month 2, Day 17",
        "headline": "The Flood Begins",
        "ref": "Genesis 7:11",
        "note": "The fountains of the great deep burst forth and the windows of heaven opened."
    },
    {
        "year": -2348, "month": 7, "day": 17,
        "label": "2348 BC - Month 7, Day 17",
        "headline": "The Ark Rests",
        "ref": "Genesis 8:4",
        "note": "Exactly 150 days after the flood began, the ark rests on Ararat."
    },
    {
        "year": -2348, "month": 10, "day": 1,
        "label": "2348 BC - Month 10, Day 1",
        "headline": "Mountain Tops Visible",
        "ref": "Genesis 8:5",
        "note": "The waters continued to recede until the peaks of the mountains were seen."
    },
    {
        "year": -2347, "month": 2, "day": 27,
        "label": "2347 BC - Month 2, Day 27",
        "headline": "Noah Leaves the Ark",
        "ref": "Genesis 8:14",
        "note": "Noah and his family exit the ark. The total duration was approximately 371 days."
    }
]

# 5. CONVERT DATA FOR THE TIMELINE COMPONENT (The "Box")
timeline_items = {"events": []}
for item in raw_data:
    verse = get_bible_text(item["ref"])
    timeline_items["events"].append({
        "start_date": {"year": item["year"], "month": item["month"], "day": item["day"]},
        "display_date": item["label"],
        "text": {
            "headline": item["headline"],
            "text": f"<i>{item['ref']}</i><br><br>{verse}"
        }
    })

# 6. RENDER THE INTERACTIVE BOX (TOP)
st.title("Chronology of the Great Flood")
try:
    timeline(timeline_items, height=500)
except Exception:
    st.warning("Interactive timeline box is loading or unavailable. See detailed view below.")

st.divider()

# 7. RENDER THE DETAILED VERTICAL LIST (BOTTOM)
st.subheader("Detailed Study & Scripture")

for item in raw_data:
    with st.container():
        # HTML for the dot-and-line timeline look
        st.markdown(f"""
            <div class="timeline-item">
                <div class="date-header">{item['label']}</div>
                <div class="headline-style">{item['headline']}</div>
            </div>
        """, unsafe_allow_html=True)

        # Content for the event
        bible_text = get_bible_text(item['ref'])
        st.info(f"**{item['ref']}**: {bible_text}")
        st.caption(f"**Note:** {item['note']}")
        st.write("")  # Spacer