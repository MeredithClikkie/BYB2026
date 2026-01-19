import streamlit as st
import requests
from streamlit_timeline import timeline

# 1. PAGE SETUP
st.set_page_config(page_title="Genesis Flood Chronology", layout="wide")

st.markdown("""
    <style>
           /* Main background and text */
           .stApp { background-color: #0e1117; color: #ffffff; }
           .block-container { padding-top: 0rem; }
           .stTitle { 
               color: #e2e8f0; 
               font-family: 'serif'; 
               text-shadow: 2px 2px 4px #000000; 
               font-size: 3rem !important;
               text-align: center;
               margin-bottom: 20px;
           }
    </style>
    """, unsafe_allow_html=True)

# 2. BIBLE API (Cached)
@st.cache_data
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        r = requests.get(url)
        return r.json()['text'] if r.status_code == 200 else "Text not found."
    except:
        return "Connection Error"

# 3. CONSTRUCT DATA WITH LARGE HIGH-RES IMAGES
def get_flood_data():
    return {
        "events": [
            {
                "group": "The Beginning",
                "start_date": {"year": -2348, "month": 2, "day": 10},
                "display_date": "2348 BC • PREPARATION",
                "background": {"color": "#1a202c"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Noahs_Ark.jpg", # Full Res
                    "caption": "Painting by Edward Hicks (1846)"
                },
                "text": {
                    "headline": "<span style='color:#ed8936;'>📦 Entry into the Ark</span>",
                    "text": f"<p style='color:#cbd5e0; font-size:1.1rem;'>{get_bible_text('Genesis 7:7')}</p>"
                }
            },
            {
                "group": "The Judgment",
                "start_date": {"year": -2348, "month": 2, "day": 17},
                "display_date": "2348 BC • THE DEEP",
                "background": {"color": "#1a365d"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/The_Deluge_by_Francis_Danby.jpg", # Full Res
                    "caption": "The Deluge by Francis Danby"
                },
                "text": {
                    "headline": "<span style='color:#63b3ed;'>🌊 The Flood Begins</span>",
                    "text": f"<p style='color:#cbd5e0; font-size:1.1rem;'>{get_bible_text('Genesis 7:11')}</p>"
                }
            },
            {
                "group": "The Resting",
                "start_date": {"year": -2348, "month": 7, "day": 17},
                "display_date": "2348 BC • RESTING",
                "background": {"color": "#2d3748"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/0/03/Simon_de_Myle_-_Noah%27s_ark_on_Mount_Ararat.jpg", # Full Res
                    "caption": "Noah's Ark on Mount Ararat by Simon de Myle"
                },
                "text": {
                    "headline": "<span style='color:#a0aec0;'>⛰️ The Ark Rests</span>",
                    "text": f"<p style='color:#cbd5e0; font-size:1.1rem;'>{get_bible_text('Genesis 8:4')}</p>"
                }
            },
            {
                "group": "The New Covenant",
                "start_date": {"year": -2347, "month": 2, "day": 27},
                "display_date": "2347 BC • COVENANT",
                "background": {"color": "#22543d"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/1/1a/The_Exit_from_the_Ark.jpg", # Full Res
                    "caption": "The Exit from the Ark"
                },
                "text": {
                    "headline": "<span style='color:#68d391;'>🌈 Noah Leaves the Ark</span>",
                    "text": f"<p style='color:#cbd5e0; font-size:1.1rem;'>{get_bible_text('Genesis 8:14')}</p>"
                }
            }
        ]
    }

# 4. RENDER
st.title("🌑 Genesis Flood: Dark Chronology")

data = get_flood_data()

# INCREASED HEIGHT: This is the primary way to make images larger in this component
try:
    timeline(data, height=850)
except Exception:
    st.error("Timeline failed to load.")

st.markdown("<br><hr style='border: 1px solid #2d3748;'>", unsafe_allow_html=True)
st.caption("Detailed chronological reconstruction based on Genesis 7-8. (Best viewed on Desktop)")