import streamlit as st
import requests

@st.cache_data
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        r = requests.get(url)
        return r.json()['text'] if r.status_code == 200 else ""
    except: return ""

def get_data():
    """This returns the dictionary format needed for the interactive timeline box"""
    return {
        "events": [
            {
                "start_date": {"year": -2348, "month": 2, "day": 10},
                "display_date": "2348 BC",
                "background": {"color": "#000000"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Noahs_Ark.jpg",
                    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Noahs_Ark.jpg/150px-Noahs_Ark.jpg",
                    "type": "image",
                    "caption": f"<b>ENTRY:</b> {get_bible_text('Genesis 7:7')}"
                },
                "text": {"headline": "<span style='color:#ed8936;'>The Gathering</span>", "text": " "}
            },
            {
                "start_date": {"year": -2348, "month": 2, "day": 17},
                "display_date": "2348 BC",
                "background": {"color": "#000000"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/The_Deluge_by_Francis_Danby.jpg",
                    "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/The_Deluge_by_Francis_Danby.jpg/150px-The_Deluge_by_Francis_Danby.jpg",
                    "type": "image",
                    "caption": f"<b>THE DEEP:</b> {get_bible_text('Genesis 7:11')}"
                },
                "text": {"headline": "<span style='color:#63b3ed;'>The Great Flood</span>", "text": " "}
            }
            # Add the rest of your events here...
        ]
    }



