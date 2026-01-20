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

import requests

def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        r = requests.get(url)
        return r.json()['text'] if r.status_code == 200 else "Text not found."
    except:
        return "Connection error. Check your internet."


def get_master_data(wave_name, chapter="1"):
    """
    Acts as the Intelligence Database. Returns specific dates based on the Book.
    """
    # Force the wave_name to Title Case immediately
    wave_name = wave_name.strip().title()

    # --- OLD TESTAMENT DRAWERS ---
    if wave_name == "Genesis":
        return {
            "1": [{"start_date": {"year": -4004}, "display_date": "Creation", "background": {"color": "#000000"},
                   "text": {"headline": "Forming the World", "text": "Day 1-3: Light out of Darkness."}}],
            "7": [{"start_date": {"year": -2348}, "display_date": "2348 BC",
                   "text": {"headline": "The Great Flood", "text": "Noah's Ark."}}]
        }

    elif wave_name == "Exodus":
        return {"3": [{"start_date": {"year": -1446}, "display_date": "1446 BC",
                       "text": {"headline": "🔥 The Burning Bush", "text": "The call of Moses."}}]}

    # --- THE GOSPELS (Unified Logic) ---
    elif wave_name in ["Matthew", "Mark", "Luke", "John"]:
        all_events = []
        # Nativity Logic
        if (wave_name in ["Matthew", "Luke"]) and str(chapter) == "2":
            all_events.append({"start_date": {"year": -4}, "display_date": "4 BC", "background": {"color": "#1a202c"},
                               "text": {"headline": "✨ The Nativity", "text": "The birth of Jesus in Bethlehem."}})

        # Passion Week Logic
        passion_chapters = {"Matthew": "27", "Mark": "15", "Luke": "23", "John": "19"}
        if str(chapter) == passion_chapters.get(wave_name):
            all_events.append({"start_date": {"year": 30}, "display_date": "AD 30", "background": {"color": "#000000"},
                               "text": {"headline": "🌑 The Crucifixion", "text": "The sacrifice at Calvary."}})

        # Fallback: General Ministry Era
        if not all_events:
            all_events.append({"start_date": {"year": 26}, "display_date": "AD 26",
                               "text": {"headline": f"Ministry: {wave_name}",
                                        "text": "The life and ministry of Christ."}})
        return {"All": all_events}

    # --- THE CHURCH AGE (Acts & Epistles) ---
    elif wave_name == "Acts":
        return {
            "1": [{"start_date": {"year": 30}, "display_date": "AD 30",
                   "text": {"headline": "The Ascension", "text": "Jesus ascends; the disciples wait."}}],
            "All": [{"start_date": {"year": 33}, "display_date": "AD 33",
                     "text": {"headline": "The Early Church", "text": "The spread of the Gospel begins."}}]
        }

    elif wave_name == "Revelation":
        return {"All": [{
            "start_date": {"year": 95},
            "display_date": "AD 95",
            "background": {"color": "#FCE300"},
            "text": {"headline": "📬 CURRENT INTEL: Revelation", "text": "Written from Patmos."}
        }]}

    # Expand this list to include EVERY letter in the NT
    elif wave_name in [
        "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
        "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
        "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
        "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude"
    ]:
        intel = {
            "Galatians": {"year": 48, "loc": "Antioch", "desc": "Regarding the Gospel of Grace."},
            "Romans": {"year": 57, "loc": "Corinth", "desc": "Paul's masterwork on salvation."},
            "Ephesians": {"year": 61, "loc": "Rome", "desc": "Written during house arrest."},
            "Philippians": {"year": 61, "loc": "Rome", "desc": "The Epistle of Joy."},
            "Colossians": {"year": 61, "loc": "Rome", "desc": "Focusing on the supremacy of Christ."},
            "Hebrews": {"year": 67, "loc": "Unknown", "desc": "The supremacy of Jesus as High Priest."}
        }
        # ctx finds the book in the list above, or uses a default AD 55 date for others
        ctx = intel.get(wave_name, {"year": 55, "loc": "Ephesus/Macedonia", "desc": "Apostolic instructions."})

        return {"All": [{
            "start_date": {"year": ctx["year"]}, "display_date": f"AD {ctx['year']}",
            "background": {"color": "#FCE300"},  # Yellow focus color
            "text": {"headline": f"📬 CURRENT INTEL: {wave_name}",
                     "text": f"<b>Written from:</b> {ctx['loc']}<br>{ctx['desc']}"}
        }]}

def get_timeline_events(book, chapter):
    # This calls your 'drawer' system
    wave_data = get_master_data(book, chapter)

    # 1. Look for chapter first, then the 'All' fallback (Important for Letters!)
    events = list(wave_data.get(str(chapter), wave_data.get("All", [])))

    # 2. Add Missionary Journeys (The 'Acts' fix)
    nt_travel_books = ["Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians"]
    if book in nt_travel_books:
        events.extend([
            {"start_date": {"year": 46}, "display_date": "AD 46", "background": {"color": "#1b4f72"}, "text": {"headline": "⛵ 1st Journey", "text": "Paul & Barnabas."}},
            {"start_date": {"year": 59}, "display_date": "AD 59", "background": {"color": "#212f3d"}, "text": {"headline": "⚓ Voyage to Rome", "text": "Paul as a prisoner."}}
        ])

    # 3. Sort and find the starting slide
    events = sorted(events, key=lambda x: x["start_date"]["year"])
    start_index = next((i for i, e in enumerate(events) if "CURRENT INTEL" in e["text"]["headline"]), 0)
    return events, start_index





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