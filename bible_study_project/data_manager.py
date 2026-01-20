import requests
import random
import re
import os
import json
import streamlit as st


# --- DATA STRUCTURES ---
BIBLE_CHAPTER_COUNTS = {
    "Genesis": 50, "Exodus": 40, "Leviticus": 27, "Numbers": 36, "Deuteronomy": 34,
    "Joshua": 24, "Judges": 21, "Ruth": 4, "1 Samuel": 31, "2 Samuel": 24,
    "1 Kings": 22, "2 Kings": 25, "1 Chronicles": 29, "2 Chronicles": 36,
    "Ezra": 10, "Nehemiah": 13, "Esther": 10, "Job": 42, "Psalms": 150,
    "Proverbs": 31, "Ecclesiastes": 12, "Song of Solomon": 8, "Isaiah": 66,
    "Jeremiah": 52, "Lamentations": 5, "Ezekiel": 48, "Daniel": 12, "Hosea": 14,
    "Joel": 3, "Amos": 9, "Obadiah": 1, "Jonah": 4, "Micah": 7, "Nahum": 3,
    "Habakkuk": 3, "Zephaniah": 3, "Haggai": 2, "Zechariah": 14, "Malachi": 4,
    "Matthew": 28, "Mark": 16, "Luke": 24, "John": 21, "Acts": 28,
    "Romans": 16, "1 Corinthians": 16, "2 Corinthians": 13, "Galatians": 6,
    "Ephesians": 6, "Philippians": 4, "Colossians": 4, "1 Thessalonians": 5,
    "2 Thessalonians": 3, "1 Timothy": 6, "2 Timothy": 4, "Titus": 3,
    "Philemon": 1, "Hebrews": 13, "James": 5, "1 Peter": 5, "2 Peter": 3,
    "1 John": 5, "2 John": 1, "3 John": 1, "Jude": 1, "Revelation": 22
}

READING_PLANS = {
    "90-Day NT": {1: {"book": "Matthew", "chap": 1}, 2: {"book": "Matthew", "chap": 2},
                  3: {"book": "Matthew", "chap": 3}},
    "OT Foundations": {1: {"book": "Genesis", "chap": 1}, 2: {"book": "Genesis", "chap": 2},
                       3: {"book": "Genesis", "chap": 3}},
    "Chronological Start": {1: {"book": "Genesis", "chap": 1}, 2: {"book": "Genesis", "chap": 4}}
}

LASB_PROMPTS = {
    "S": "What specific verse is the Spirit highlighting?",
    "O": "What facts or context do you notice here?",
    "A": "How does this apply to your current 'Trench'?",
    "P": "Write a prayer regarding this revelation."
}

BP_MAP = {
    "Genesis": "GQI72THyO5I", "Exodus": "jH_aojNJM3E", "Leviticus": "IJ-FekWUZzE",
    "Matthew": "3aybbV6o27Y", "Mark": "HGHqu9-DtXk", "Luke": "f6566L1L5I0", "John": "G-2e99gm7f8"
}


# --- FUNCTIONS ---
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        r = requests.get(url)
        return r.json()['text'] if r.status_code == 200 else "Text not found."
    except:
        return "Connection error."


def get_master_data(wave_name, chapter="1"):
    """
    Acts as the Intelligence Database. Returns specific dates based on the Book.
    """
    # Drawer 1: Genesis (Detailed by Chapter)
    if wave_name == "Genesis":
        return {
            "1": [{"start_date": {"year": -4004}, "display_date": "Day 1-3", "background": {"color": "#000000"},
                   "media": {
                       "url": "https://upload.wikimedia.org/wikipedia/commons/6/6d/The_Creation_of_Light_by_Gustave_Dore.jpg",
                       "type": "image"},
                   "text": {"headline": "Forming the World", "text": "<b>Day 1:</b> Light out of Darkness."}}],
            "7": [{"start_date": {"year": -2348}, "display_date": "2348 BC", "background": {"color": "#1a365d"},
                   "text": {"headline": "The Great Flood", "text": "Masoretic timeline calculated by Ussher."}}]
        }

    # Drawer 2: Exodus (Detailed by Chapter)
    elif wave_name == "Exodus":
        return {
            "3": [{"start_date": {"year": -1446}, "display_date": "1446 BC", "background": {"color": "#744210"},
                   "text": {"headline": "🔥 The Burning Bush", "text": "15th-century date based on 1 Kings 6:1."}}]
        }

    # Drawer 3: The Law (General Era Intel)
    elif wave_name in ["Leviticus", "Numbers", "Deuteronomy"]:
        return {"All": [{"start_date": {"year": -1445}, "display_date": "1445 BC", "background": {"color": "#2D3748"},
                         "text": {"headline": f"The Law: {wave_name}",
                                  "text": "Israel receives instructions at Mt. Sinai."}}]}

    # Drawer: Era of Judges (Joshua through Ruth)
    elif wave_name in ["Joshua", "Judges", "Ruth"]:
        return {"All": [{"start_date": {"year": -1400}, "display_date": "c. 1400 BC", "background": {"color": "#4a5568"},
                 "text": {"headline": "Era of the Judges",
                          "text": "Israel enters the land and is led by various judges."}}]}

    # Drawer: Era of the Monarchy (Samuel through Chronicles, plus Wisdom Books)
    elif wave_name in ["1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Psalms",
                       "Proverbs", "Ecclesiastes", "Song of Solomon"]:
        return {
            "All": [{"start_date": {"year": -1010}, "display_date": "c. 1010 BC", "background": {"color": "#9a7d0a"},
                     "text": {"headline": "The United Monarchy",
                              "text": "The golden age of Israel under David and Solomon."}}]}

    # Drawer: The Prophets (Isaiah through Malachi)
    elif wave_name in ["Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah",
                       "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"]:
        # Specific Chapter Intel: Daniel's Exile
        if wave_name == "Daniel" and str(chapter) == "1":
            return {"1": [{
                "start_date": {"year": -605},
                "display_date": "605 BC",
                "background": {"color": "#1a202c"},
                "text": {"headline": "🧱 The First Deportation", "text": "Daniel and his friends are taken to Babylon."}
            }]}

        return {"All": [
            {"start_date": {"year": -740}, "display_date": "8th-5th Century BC", "background": {"color": "#17202a"},
             "text": {"headline": "The Prophetic Voice",
                      "text": "God speaks to His people before and during the Exile."}}]}

        # --- NEW TESTAMENT DRAWERS ---

    # 1. Drawer: Church History (Acts)
    elif wave_name == "Acts":
        return {
            "1": [{
                "start_date": {"year": 30},
                "display_date": "AD 30",
                "background": {"color": "#2D3748"},
                "text": {"headline": "The Ascension", "text": "Jesus ascends; the disciples wait in Jerusalem."}
            }],
            "All": [{
                "start_date": {"year": 33},
                "display_date": "1st Century AD",
                "background": {"color": "#2D3748"},
                "text": {"headline": "The Early Church", "text": "The spread of the Gospel from Jerusalem to Rome."}
            }]
        }

    # 2. Drawer: The Epistles (All of them)
    elif wave_name in [
        "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
        "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
        "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
        "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude"
    ]:
        return {"All": [{
            "start_date": {"year": 55},
            "display_date": "c. AD 55",
            "background": {"color": "#FCE300"},
            "text": {"headline": f"Mission Intel: {wave_name}", "text": "Apostolic instructions to the early Church."}
        }]}

    # 3. Drawer: The Apocalypse (Revelation)
    elif wave_name == "Revelation":
        return {"All": [{
            "start_date": {"year": 95},
            "display_date": "c. AD 95",
            "background": {"color": "#44337a"},
            "text": {"headline": "The Apocalypse", "text": "John's vision on the Island of Patmos."}
        }]}

    # The Silent Years (Between Malachi and Matthew)
    elif wave_name == "Intertestamental":
        return {"All": [{
            "start_date": {"year": -400},
            "display_date": "400 BC - 4 BC",
            "text": {"headline": "The Silent Years", "text": "The period between the Old and New Testaments."}
        }]}

        # Drawer 5: The Gospels (Unified Logic)
    elif wave_name in ["Matthew", "Mark", "Luke", "John"]:
        all_events = []

        # 1. Check for Nativity in Matthew/Luke Chapter 2
        if (wave_name == "Matthew" and str(chapter) == "2") or (wave_name == "Luke" and str(chapter) == "2"):
            all_events.append({
                "start_date": {"year": -4},
                "display_date": "4 BC",
                "background": {"color": "#1a202c"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/The_Nativity_by_Federico_Barocci.jpg/440px-The_Nativity_by_Federico_Barocci.jpg",
                    "type": "image"},
                "text": {"headline": "✨ The Nativity", "text": "The birth of Jesus in Bethlehem."}
            })

        # 2. General Gospel Era (If not Ch. 2, or in Mark/John)
        if not all_events:
            all_events.append({
                "start_date": {"year": 26},
                "display_date": "AD 26",
                "background": {"color": "#2d3748"},
                "text": {"headline": f"The Life of Christ: {wave_name}",
                         "text": "The ministry and historical context of Jesus."}
            })

        # Change the key from "current_chapter" to "All" to match your system
        return {"All": all_events}

        # Safety Net: Final Catch-all
    return {
        "All": [{
            "start_date": {"year": 0},
            "display_date": "General History",
            "text": {"headline": f"{wave_name} Overview", "text": "Historical overview loading..."}
        }]
    }


def get_timeline_events(book, chapter):
    wave_data = get_master_data(book, chapter)
    if not wave_data:
        return [], 0

    # 1. TRY SPECIFIC CHAPTER (e.g., Acts '1')
    events = wave_data.get(str(chapter))

    # 2. FALLBACK TO 'ALL' (e.g., Romans doesn't have a '1' key, but has 'All')
    if events is None:
        events = wave_data.get("All", [])

    # Create a fresh copy so we don't pollute the master data
    events = list(events)

    # 3. ADD PERMANENT JOURNEYS
    nt_travel_books = ["Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians",
                       "Colossians"]
    if book in nt_travel_books:
        events.extend([
            {"start_date": {"year": 46}, "display_date": "AD 46", "background": {"color": "#1b4f72"},
             "text": {"headline": "⛵ 1st Journey", "text": "Paul & Barnabas sent from Antioch."}},
            {"start_date": {"year": 59}, "display_date": "AD 59", "background": {"color": "#212f3d"},
             "text": {"headline": "⚓ Voyage to Rome", "text": "Paul travels as a prisoner."}}
        ])

    if not events: return [], 0

    # 4. SORT (Ensures chronology works correctly)
    events = sorted(events, key=lambda x: x.get("start_date", {}).get("year", 0))
    return events, 0



# --- TRIVIA DATABASE ---
# Structured data for your hand-crafted games
BIBLE_DATA = {
    "Genesis": {
        1: {
            "trivia": [
                {
                    "question": "What did God create on the first day?",
                    "options": ["Animals", "Light", "Plants", "The Sun"],
                    "answer": "Light",
                    "reference": "Genesis 1:3-5"
                },
                {
                    "question": "How did God describe His creation at the end of day one?",
                    "options": ["It was okay", "It was good", "It was perfect", "It was finished"],
                    "answer": "It was good",
                    "reference": "Genesis 1:4"
                }
            ]
        },
        2: {
            "trivia": [
                {
                    "question": "Out of what did God form man?",
                    "options": ["Stone", "Dust of the ground", "Water", "A cloud"],
                    "answer": "Dust of the ground",
                    "reference": "Genesis 2:7"
                }
            ]
        }
    },
    "Exodus": {
        1: {
            "trivia": [], # Add your Exodus trivia here later
        }
    }
}

def get_trivia_questions(book, chapter):
    """Fetches hand-crafted trivia questions for a specific chapter."""
    return BIBLE_DATA.get(book, {}).get(chapter, {}).get("trivia", [])

def get_auto_trivia(book, chapter):
    url = f"https://bible-api.com/{book}+{chapter}"
    try:
        text = requests.get(url).json()['text']
        verses = [v for v in text.split('\n') if 60 < len(v) < 150]
        questions = []
        for v in random.sample(verses, min(len(verses), 3)):
            words = re.findall(r'\b\w{5,}\b', v)
            if words:
                ans = random.choice(words)
                questions.append(
                    {"question": v.replace(ans, "_______"), "options": [ans, "Faith", "Grace", "Truth"], "answer": ans})
        return questions
    except:
        return []


def get_bible_project_url(book):
    v_id = BP_MAP.get(book)
    return f"https://www.youtube.com/embed/{v_id}" if v_id else None


def get_gotquestions_url(book, chapter):
    return f"https://www.gotquestions.org/Book-of-{book.replace(' ', '-')}.html"