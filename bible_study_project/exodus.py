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
        # 1. Clean the string and split into words
        parts = full_reference.strip().split()
        # 2. The second part is always the numbers (7 or 7:1)
        numbers = parts[1]
        # 3. Split by ":" in case verses were included
        chapter = numbers.split(":")[0]
    except Exception as e:
        chapter = "1"

    # --- DEBUGGING TIP ---
    # Uncomment the line below to see exactly what 'chapter' the code is looking for
    # st.write(f"DEBUG: Searching for chapter '{chapter}'")

    all_chapters = {
        # --- CHAPTER 3: THE BURNING BUSH ---

        "3": [
            {
                "start_date": {"year": -1446},
                "display_date": "1446 BC (Early Date)",
                "background": {"color": "#744210"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Simeon_Solomon_Moses_and_the_Burning_Bush.jpg/440px-Simeon_Solomon_Moses_and_the_Burning_Bush.jpg",
                    "type": "image"},
                "text": {
                    "headline": "🔥 The Burning Bush",
                    "text": "The 15th-century date based on 1 Kings 6:1, placing the Exodus during the 18th Dynasty of Egypt."
                }
            },
            {
                "start_date": {"year": -1250},
                "display_date": "c. 1250 BC (Late Date)",
                "background": {"color": "#4a5568"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Simeon_Solomon_Moses_and_the_Burning_Bush.jpg/440px-Simeon_Solomon_Moses_and_the_Burning_Bush.jpg",
                    "type": "image"},
                "text": {
                    "headline": "🔥 The Burning Bush (Ramesside)",
                    "text": "The 13th-century date often favored by archaeologists, placing the Exodus during the reign of Ramesses II."
                }
            }
        ],

        # --- CHAPTER 12: THE PASSOVER ---
        "12": [
            {
                "start_date": {"year": -1446, "month": 1, "day": 14},
                "display_date": "1446 BC, Nisan 14",
                "background": {"color": "#000000"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Charles_Foster_The_Signs_on_the_Door.jpg/440px-Charles_Foster_The_Signs_on_the_Door.jpg",
                    "type": "image"},
                "text": {"headline": "🌑 The Tenth Plague",
                         "text": "The final plague on Egypt and the institution of the Passover."}
            }
        ],

        # --- CHAPTER 14: THE RED SEA ---
        "14": [
            {
                "start_date": {"year": -1446, "month": 1, "day": 20},
                "display_date": "1446 BC, The Crossing",
                "background": {"color": "#2c5282"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/The_Seventh_Plague_by_John_Martin.jpg/800px-The_Seventh_Plague_by_John_Martin.jpg",
                    "type": "image"},
                "text": {"headline": "🌊 Crossing the Red Sea", "text": "Israel is delivered from Pharaoh's army."}
            }
        ]
    }
    events = all_chapters.get(chapter, [])
    return {"events": events}