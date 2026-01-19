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
    # Extracts Book and Chapter (e.g., "John 3:16" -> "John", "3")
    try:
        parts = full_reference.strip().split()
        book = parts[0].title()
        chapter = parts[1].split(":")[0]
    except:
        return {"events": []}

    all_events = []

    # --- EVENT: PROLOGUE / NATIVITY ---
    if chapter == "1" and book == "John":
        all_events.append({
            "start_date": {"year": -4004},  # Eternal past
            "display_date": "Eternity Past",
            "background": {"color": "#000000"},
            "text": {"headline": "The Word", "text": "In the beginning was the Word..."}
        })

    if (book == "Matthew" and chapter == "2") or (book == "Luke" and chapter == "2"):
        all_events.append({
            "start_date": {"year": -4},
            "display_date": "4 BC",
            "background": {"color": "#1a202c"},
            "media": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/The_Nativity_by_Federico_Barocci.jpg/440px-The_Nativity_by_Federico_Barocci.jpg",
                "type": "image"},
            "text": {"headline": "✨ The Nativity", "text": "The birth of Jesus in Bethlehem."}
        })

    # --- EVENT: BAPTISM & TEMPTATION ---
    if chapter == "3" and book in ["Matthew", "Mark", "Luke"]:
        all_events.append({
            "start_date": {"year": 26},
            "display_date": "AD 26",
            "background": {"color": "#2d3748"},
            "media": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Baptism_of_Christ_by_Piero_della_Francesca.jpg/440px-Baptism_of_Christ_by_Piero_della_Francesca.jpg",
                "type": "image"},
            "text": {"headline": "🌊 Baptism of Jesus", "text": "Ministry begins at the Jordan River."}
        })

    # --- EVENT: THE CRUCIFIXION ---
    passion_chapters = {"Matthew": "27", "Mark": "15", "Luke": "23", "John": "19"}
    if chapter == passion_chapters.get(book):
        all_events.append({
            "start_date": {"year": 30, "month": 4, "day": 7},
            "display_date": "AD 30",
            "background": {"color": "#000000"},
            "media": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Crucifixion_Dali.jpg/440px-Crucifixion_Dali.jpg",
                "type": "image"},
            "text": {"headline": "🌑 The Crucifixion", "text": "The sacrifice at Calvary."}
        })

    return {"events": all_events}
