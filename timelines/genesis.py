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
    # Extracts the chapter number from the reference (e.g., "Genesis 7:1" -> "7")
    try:
        chapter = full_reference.split(" ")[1].split(":")[0]
    except:
        chapter = "1"

    # THE MASTER DATABASE OF GENESIS EVENTS
    all_chapters = {
        # --- CHAPTER 1: CREATION ---
        "1": [
            {
                "start_date": {"year": -4004},
                "display_date": "Day 1",
                "background": {"color": "#1a202c"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/The_Creation_of_Light_by_Gustave_Dore.jpg/440px-The_Creation_of_Light_by_Gustave_Dore.jpg",
                    "type": "image"},
                "text": {"headline": "Let There Be Light", "text": get_bible_text("Genesis 1:3")}
            }
        ],

        # --- CHAPTER 7: THE FLOOD BEGINS ---
        "7": [
            {
                "start_date": {"year": -2348, "month": 2, "day": 10},
                "display_date": "2348 BC, Mo 2, Day 10",
                "background": {"color": "#000000"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Noahs_Ark.jpg",
                    "type": "image",
                    "caption": f"<b>ENTRY:</b> {get_bible_text('Genesis 7:7')}"
                },
                "text": {"headline": "<span style='color:#ed8936;'>The Gathering</span>", "text": " "}
            },
            {
                "start_date": {"year": -2348, "month": 2, "day": 17},
                "display_date": "2348 BC, Mo 2, Day 17",
                "background": {"color": "#1a365d"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/The_Deluge_by_Francis_Danby.jpg",
                    "type": "image",
                    "caption": f"<b>THE DEEP:</b> {get_bible_text('Genesis 7:11')}"
                },
                "text": {"headline": "<span style='color:#63b3ed;'>The Great Flood</span>", "text": " "}
            }
        ],

        # --- CHAPTER 8: THE WATERS RECEDE ---
        "8": [
            {
                "start_date": {"year": -2348, "month": 7, "day": 17},
                "display_date": " 2348 BC, Month 7, Day 17",
                "background": {"color": "#2d3748"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Simon_de_Myle_-_Noah%27s_ark_on_Mount_Ararat.jpg/800px-Simon_de_Myle_-_Noah%27s_ark_on_Mount_Ararat.jpg",
                    "type": "image"},
                "text": {"headline": "The Ark Rests", "text": get_bible_text("Genesis 8:4")}
            },
            {
                "start_date": {"year": -2347, "month": 2, "day": 27},
                "display_date": "2347 BC, Mo 2, Day 27",
                "background": {"color": "#22543d"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/The_Exit_from_the_Ark.jpg/800px-The_Exit_from_the_Ark.jpg",
                    "type": "image"},
                "text": {"headline": "A New Beginning", "text": get_bible_text("Genesis 8:14")}
            }
        ]
    }

    # Retrieve the list for the current chapter, or return an empty list if we haven't built it yet
    events = all_chapters.get(chapter, [])

    return {"events": events}