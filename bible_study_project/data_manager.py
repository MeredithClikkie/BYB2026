# data_manager.py
import requests
import streamlit as st
import data_manager as dm
import json
import os

# Load saved progress from a file
def load_progress():
    if os.path.exists("progress.json"):
        with open("progress.json", "r") as f:
            return json.load(f)
    return []

# Initialize session state with saved data
if "completed_books" not in st.session_state:
    st.session_state.completed_books = load_progress()

def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        return response.json()['text'] if response.status_code == 200 else "Text not found."
    except:
        return "Connection error."

def get_master_data(wave_name, chapter = "1"):
    """
    Returns the full database for a specific 'Wave' (Book).
    """
    # --- GENESIS DATA ---
    if wave_name == "Genesis":
        return {
                # --- CHAPTER 1: CREATION ---
            "1": [
                {
                    "start_date": {"year": -4004},
                    "display_date": "Day 1-3",
                    "background": {"color": "#000000"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/6/6d/The_Creation_of_Light_by_Gustave_Dore.jpg",
                        "type": "image"},
                    "text": {"headline": "Forming the World",
                             "text": f"<b>Day 1:</b> Light out of Darkness.<br><b>Day 2:</b> The Firmament.<br><b>Day 3:</b> Dry land and seas."}
                },
                {
                    "start_date": {"year": -4004},
                    "display_date": "Day 4-6",
                    "background": {"color": "#1a365d"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Creation_of_the_Sun_and_Moon_by_Dore.jpg",
                        "type": "image"},
                    "text": {"headline": "Filling the World",
                             "text": f"<b>Day 4:</b> Sun, Moon, and Stars.<br><b>Day 5:</b> Creatures of Sky and Sea.<br><b>Day 6:</b> Land animals and Mankind."}
                }
            ],

            # --- CHAPTER 7: THE FLOOD BEGINS ---
            "7": [
                # --- MASORETIC TEXT (Standard Tradition) ---
                {
                    "start_date": {"year": -2348, "month": 2, "day": 17},
                    "display_date": "2348 BC (Masoretic)",
                    "background": {"color": "#1a365d"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/The_Deluge_by_Francis_Danby.jpg",
                        "type": "image",
                        "caption": "Date calculated by Archbishop James Ussher."
                    },
                    "text": {"headline": "The Great Flood", "text": "The traditional Masoretic timeline."}
                },

                # --- SAMARITAN PENTATEUCH ---
                {
                    "start_date": {"year": -3145, "month": 2, "day": 17},
                    "display_date": "3145 BC (Samaritan)",
                    "background": {"color": "#2d3748"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Noahs_Ark.jpg",
                        "type": "image"},
                    "text": {"headline": "Samaritan Chronology", "text": "This tradition places the flood earlier."}
                },

                # --- SEPTUAGINT (Greek Tradition) ---
                {
                    "start_date": {"year": -3298, "month": 2, "day": 17},
                    "display_date": "3298 BC (Septuagint)",
                    "background": {"color": "#000000"},
                    "media": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Noahs_Ark.jpg",
                        "type": "image"},
                    "text": {"headline": "Septuagint Chronology", "text": "The oldest biblical manuscript tradition."}
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

    # --- EXODUS DATA ---
    elif wave_name == "Exodus":
        return {
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

    # --- ERA OF SOLOMON (Proverbs, Ecclesiastes, Song of Solomon) ---
    elif wave_name in ["Proverbs", "Ecclesiastes", "Song of Solomon"]:
        # We return a dictionary where the key is "All" so the timeline loads automatically
        return {
            "All": [{
                "start_date": {"year": -970},
                "display_date": "10th Century BC",
                "background": {"color": "#9a7d0a"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Solomon_by_Simeon_Solomon.jpg/440px-Solomon_by_Simeon_Solomon.jpg",
                    "type": "image"},
                "text": {"headline": f"The Wisdom of {wave_name}",
                         "text": "Written during the Golden Age of Israel's Monarchy."}
            }]
        }

    # --- ERA OF DAVID (Psalms) ---
    elif wave_name == "Psalms":
        return {
            "All": [{
                "start_date": {"year": -1010},
                "display_date": "The United Kingdom",
                "background": {"color": "#1e8449"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/King_David_by_Guido_Reni.jpg/440px-King_David_by_Guido_Reni.jpg",
                    "type": "image"},
                "text": {"headline": "The Songs of Israel",
                         "text": "Poetry and worship collected largely during the reign of King David."}
            }]
        }


        # --- PROPHETS WAVE ---
    elif wave_name in ["Isaiah", "Jeremiah", "Ezekiel", "Daniel", "Malachi"]:
        return {
            "All": [
                {
                    "start_date": {"year": -586},
                    "display_date": "The Exile",
                    "background": {"color": "#17202a"},
                    "text": {"headline": "The Fall of Jerusalem",
                             "text": f"{wave_name} speaks into the era of the Babylonian captivity."}
                },
                {
                    "start_date": {"year": -538},
                    "display_date": "The Return",
                    "background": {"color": "#f1c40f"},
                    "text": {"headline": "Restoration", "text": "The remnant returns to rebuild the Temple."}
                }
            ]
        }

    # --- GOSPEL HARMONY WAVE ---
    elif wave_name in ["Matthew", "Mark", "Luke", "John"]:
        all_events = []

        # John 1: Prologue
        if chapter == "1" and wave_name == "John":
            all_events.append({
                "start_date": {"year": -4004},
                "display_date": "Eternity Past",
                "background": {"color": "#000000"},
                "text": {"headline": "The Word", "text": "In the beginning was the Word..."}
            })

        # Nativity
        if (wave_name == "Matthew" and chapter == "2") or (wave_name == "Luke" and chapter == "2"):
            all_events.append({
                "start_date": {"year": -4},
                "display_date": "4 BC",
                "background": {"color": "#1a202c"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/The_Nativity_by_Federico_Barocci.jpg/440px-The_Nativity_by_Federico_Barocci.jpg",
                    "type": "image"},
                "text": {"headline": "✨ The Nativity", "text": "The birth of Jesus in Bethlehem."}
            })

        # Baptism
        if chapter == "3" and wave_name in ["Matthew", "Mark", "Luke"]:
            all_events.append({
                "start_date": {"year": 26},
                "display_date": "AD 26",
                "background": {"color": "#2d3748"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Baptism_of_Christ_by_Piero_della_Francesca.jpg/440px-Baptism_of_Christ_by_Piero_della_Francesca.jpg",
                    "type": "image"},
                "text": {"headline": "🌊 Baptism of Jesus", "text": "Ministry begins at the Jordan River."}
            })

        # Crucifixion
        passion_chapters = {"Matthew": "27", "Mark": "15", "Luke": "23", "John": "19"}
        if chapter == passion_chapters.get(wave_name):
            all_events.append({
                "start_date": {"year": 30, "month": 4, "day": 7},
                "display_date": "AD 30",
                "background": {"color": "#000000"},
                "media": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Crucifixion_Dali.jpg/440px-Crucifixion_Dali.jpg",
                    "type": "image"},
                "text": {"headline": "🌑 The Crucifixion", "text": "The sacrifice at Calvary."}
            })

        return {"current_chapter": all_events}

    return {}

def get_timeline_events(book, chapter):
    # Initialize as an empty list so we can always append to it
    events = []

    # Step 1: Get data from master (SOFT CHECK)
    wave_data = get_master_data(book, chapter)

    # Only process wave_data if it actually exists
    if wave_data:
        if chapter == "All":
            for ch_events in wave_data.values():
                if isinstance(ch_events, list):
                    events.extend(ch_events)
        else:
            # Check for specific chapter or the Gospel harmony key
            events = wave_data.get(str(chapter), wave_data.get("current_chapter", []))

    # Step 2: ADD PERMANENT JOURNEYS (Acts & Epistles)
    nt_books = ["Acts", "Romans", "Galatians", "Ephesians", "Philippians", "Colossians", "Hebrews", "James"]
    gospels = ["Matthew", "Mark", "Luke", "John"]

    if book in nt_books or book in gospels:
        journeys = [
            {"year": 46, "head": "⛵ 1st Journey (Acts 13-14)", "color": "#1b4f72",
             "text": "Paul & Barnabas sent from Antioch to Cyprus and Galatia."},
            {"year": 49, "head": "🗺️ 2nd Journey (Acts 15-18)", "color": "#1e8449",
             "text": "The Gospel enters Europe; ministry in Philippi and Corinth."},
            {"year": 53, "head": "📖 3rd Journey (Acts 19-21)", "color": "#9a7d0a",
             "text": "Paul's extensive ministry in Ephesus."},
            {"year": 59, "head": "⚓ Voyage to Rome (Acts 27-28)", "color": "#212f3d",
             "text": "Paul travels as a prisoner to stand trial before Caesar."}
        ]

        for j in journeys:
            events.append({
                "start_date": {"year": j["year"]},
                "display_date": f"AD {j['year']}",
                "background": {"color": j["color"]},
                "text": {"headline": j["head"], "text": j["text"]}
            })

    # Step 3: ADD EPISTLE DATA
    epistle_context = {
        "Galatians": {"year": 48, "loc": "Antioch", "context": "Regarding the Gospel of Grace."},
        "Romans": {"year": 57, "loc": "Corinth", "context": "Paul's masterwork on salvation."},
        "Ephesians": {"year": 61, "loc": "Rome (Prison)", "context": "Written during house arrest."},
        "Philippians": {"year": 61, "loc": "Rome (Prison)", "context": "The 'Epistle of Joy'."},
        "Colossians": {"year": 61, "loc": "Rome (Prison)", "context": "Supremacy of Christ."}
    }

    if book in epistle_context:
        ctx = epistle_context[book]
        events.append({
            "start_date": {"year": ctx["year"]},
            "display_date": f"AD {ctx['year']}",
            "background": {"color": "#FCE300"},
            "text": {
                "headline": f"📬 CURRENT INTEL: Letter to the {book}",
                "text": f"<b>Written from:</b> {ctx['loc']}<br><br>{ctx['context']}"
            }
        })

    # Step 4: FINAL CHECK & SORTING
    if not events:
        return [], 0

    # Ensure every event has a year to avoid sorting errors
    events = sorted(events, key=lambda x: x.get("start_date", {}).get("year", 0))

    # Find the "Current Intel" index to center the timeline
    start_index = 0
    for i, event in enumerate(events):
        if "CURRENT INTEL" in event.get("text", {}).get("headline", ""):
            start_index = i
            break

    return events, start_index

import random

# Structured data for your games
# You can expand this dictionary for every book/chapter
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
            ],
            "hangman_words": ["CREATION", "HEAVENS", "EARTH", "SPIRIT"]
        },
        2: {
            "trivia": [
                {
                    "question": "Out of what did God form man?",
                    "options": ["Stone", "Dust of the ground", "Water", "A cloud"],
                    "answer": "Dust of the ground",
                    "reference": "Genesis 2:7"
                }
            ],
            "hangman_words": ["EDEN", "ADAM", "EVE", "RIVER", "EUPHRATES"]
        }
    },
    "Exodus": {
        1: {
            "trivia": [],
            "hangman_words": ["EGYPT", "PHARAOH", "MIDWIVES"]
        }
    }
}

def get_trivia_questions(book, chapter):
    """Fetches trivia questions for a specific chapter."""
    return BIBLE_DATA.get(book, {}).get(chapter, {}).get("trivia", [])

def get_hangman_word(book, chapter):
    """Fetches a random word for Hangman for a specific chapter."""
    words = BIBLE_DATA.get(book, {}).get(chapter, {}).get("hangman_words", ["BIBLE"])
    return random.choice(words).upper()

def get_available_books():
    """Returns a list of books currently in the database."""
    return list(BIBLE_DATA.keys())

def get_available_chapters(book):
    """Returns a list of chapters available for a chosen book."""
    return list(BIBLE_DATA.get(book, {}).keys())


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

import streamlit as st
import data_manager as dm

# 1. User picks a book
book_list = list(dm.BIBLE_CHAPTER_COUNTS.keys())
selected_book = st.selectbox("Choose a Book", book_list)

# 2. Get the maximum chapters for THAT specific book
max_chapters = dm.BIBLE_CHAPTER_COUNTS[selected_book]

# 3. User picks a chapter (it will only show numbers between 1 and max)
selected_chapter = st.number_input(
    f"Choose a Chapter (1 to {max_chapters})",
    min_value=1,
    max_value=max_chapters
)

st.write(f"Now loading the game for **{selected_book} Chapter {selected_chapter}**...")

import requests
import random
import re

# Master list of "boring" words to ignore when picking game words
STOP_WORDS = {"the", "and", "shall", "unto", "them", "their", "said", "with", "from", "that"}


def fetch_chapter_text(book, chapter):
    """Pulls full chapter text from Bible-Api.com."""
    url = f"https://bible-api.com/{book}+{chapter}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["text"]
    return None


def generate_auto_game(book, chapter):
    """Automated logic: Fetch -> Strip -> Select -> Generate"""
    text = fetch_chapter_text(book, chapter)
    if not text:
        return None

    # 1. STRIP: Remove punctuation and lowercase everything
    words_only = re.findall(r'\b\w{5,}\b', text.lower())  # Only words 5+ letters long

    # 2. FILTER: Remove common 'stop words'
    keywords = [w for w in words_only if w not in STOP_WORDS]

    # 3. SELECT: Pick 5 unique random words for Hangman/Trivia
    selected_words = list(set(random.sample(keywords, min(len(keywords), 10))))

    return {
        "text_preview": text[:500] + "...",
        "game_words": [w.upper() for w in selected_words]
    }


import requests
import re
import random


def get_auto_trivia(book, chapter):
    """Fetches text and creates fill-in-the-blank questions on the fly."""
    url = f"https://bible-api.com/{book}+{chapter}"
    try:
        data = requests.get(url).json()
        text = data['text']
        # Find verses that are a good length (between 60 and 150 chars)
        verses = [v for v in text.split('\n') if 60 < len(v) < 150]

        auto_questions = []
        for v in random.sample(verses, min(len(verses), 3)):
            words = re.findall(r'\b\w{5,}\b', v)  # Find words with 5+ letters
            if words:
                answer = random.choice(words)
                # Create the question by replacing the answer word with blanks
                question_text = v.replace(answer, "_______")

                # Generate 'distractors' (wrong answers) from other words in the verse
                other_words = list(set(words) - {answer})
                options = [answer] + random.sample(other_words, min(len(other_words), 3))
                random.shuffle(options)

                auto_questions.append({
                    "question": f"Fill in the blank: \n\n '{question_text}'",
                    "options": options,
                    "answer": answer,
                    "reference": f"{book} {chapter}"
                })
        return auto_questions
    except:
        return []


# Mapping of BibleProject YouTube IDs (Part 1 - expand as needed)
BP_MAP = {
    "Genesis": "GQI72THyO5I", "Exodus": "jH_aojNJM3E", "Leviticus": "IJ-FekWUZzE",
    "Numbers": "tp5MIrMZFdc", "Deuteronomy": "q5QEj9K_8X8", "Joshua": "JqOqJlFF_eU",
    "Judges": "kOYy8iCfZ4M", "Ruth": "0h1eoBeR4Jk", "1 Samuel": "QEJ8IT7C_yE",
    "2 Samuel": "1Xm1B2Y6tS8", "Psalms": "j9phNEaPrv8", "Proverbs": "AzmYV8GNAIM",
    "Isaiah": "d0A6Uchb1F8", "Jeremiah": "RSK78aejdqc", "Daniel": "9cba0QYp87E",
    "Matthew": "3aybbV6o27Y", "Mark": "HGHqu9-DtXk", "Luke": "f6566L1L5I0",
    "John": "G-2e99gm7f8", "Acts": "CGbNw855ksw", "Romans": "ej2-grduu_o",
    "Philippians": "oE9at4athAg", "Revelation": "5nvVVcYD-0w"
}

def get_bible_project_url(book):
    video_id = BP_MAP.get(book)
    if video_id:
        # Use the embed format which is often more compatible with apps
        return f"https://www.youtube.com/embed/{video_id}"
    return None

def get_gotquestions_url(book, chapter):
    formatted_book = book.replace(" ", "-")
    return f"https://www.gotquestions.org/Book-of-{formatted_book}.html"

JOURNAL_PROMPTS = {
    "Genesis": "How do you see God's sovereignty in the act of creation?",
    "Exodus": "In what ways has God 'delivered' you from a personal 'Egypt'?",
    "Romans": "How does Paul's explanation of grace change your view of your daily mistakes?",
    "Philippians": "What is one specific situation where you can choose 'joy' over 'anxiety' today?",
    "Acts": "How can you be a 'witness' in your current city or circle of influence?"
}

DEFAULT_PROMPT = "What is the Holy Spirit highlighting to you in this chapter?"


# In data_manager.py
READING_PLANS = {
    "Chronological": {
        "Day 1": "Genesis 1-3",
        "Day 2": "Genesis 4-7",
        # ...
    },
    "New Testament (90 Days)": {
        "Day 1": "Matthew 1-2",
        "Day 2": "Matthew 3-4",
    }
}

# In biblestudy_gpp.py Sidebar
st.sidebar.divider()
plan_choice = st.sidebar.selectbox("Select Reading Plan", list(dm.READING_PLANS.keys()))
day_num = st.sidebar.number_input("Day", 1, 365, value=1)

current_reading = dm.READING_PLANS[plan_choice].get(f"Day {day_num}")
st.sidebar.info(f"📅 Today's Goal: **{current_reading}**")