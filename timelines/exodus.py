import streamlit as st
import requests


@st.cache_data
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        r = requests.get(url)
        return r.json()['text'] if r.status_code == 200 else ""
    except:
        return ""


def get_data(full_reference):
    # Extracts chapter number (e.g., "Exodus 7:1" -> "7")
    try:
        chapter = full_reference.split(" ")[1].split(":")[0]
    except:
        chapter = "1"

    all_chapters = {
        # --- CHAPTER 3: THE BURNING BUSH ---
        "3": [
            {
                "start_date": {"year": -1446},
                "display_date": "The Wilderness",
                "background": {"color": "#744210"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Simeon_Solomon_Moses_and_the_Burning_Bush.jpg/440px-Simeon_Solomon_Moses_and_the_Burning_Bush.jpg",
                    "type": "image"},
                "text": {"headline": "🔥 The Burning Bush", "text": get_bible_text("Exodus 3:2")}
            }
        ],

        # --- CHAPTER 7-12: THE PLAGUES ---
        "7": [
            {
                "start_date": {"year": -1446, "month": 1, "day": 1},
                "display_date": "Plague 1",
                "background": {"color": "#7b0000"},  # Blood Red
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Plague_of_Blood.jpg/800px-Plague_of_Blood.jpg",
                    "type": "image"},
                "text": {"headline": "🩸 Water to Blood", "text": get_bible_text("Exodus 7:20")}
            }
        ],

        "12": [
            {
                "start_date": {"year": -1446, "month": 1, "day": 14},
                "display_date": "Passover",
                "background": {"color": "#000000"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Charles_Foster_The_Signs_on_the_Door.jpg/440px-Charles_Foster_The_Signs_on_the_Door.jpg",
                    "type": "image"},
                "text": {"headline": "🌑 The Tenth Plague", "text": get_bible_text("Exodus 12:29")}
            }
        ],

        # --- CHAPTER 14: THE RED SEA ---
        "14": [
            {
                "start_date": {"year": -1446, "month": 1, "day": 20},
                "display_date": "The Deliverance",
                "background": {"color": "#2c5282"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/The_Seventh_Plague_by_John_Martin.jpg/800px-The_Seventh_Plague_by_John_Martin.jpg",
                    "type": "image"},
                "text": {"headline": "🌊 Crossing the Red Sea", "text": get_bible_text("Exodus 14:21")}
            }
        ]
    }

    events = all_chapters.get(chapter, [])
    return {"events": events}