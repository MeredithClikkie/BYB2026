import streamlit as st
import pandas as pd
import plotly.express as px
import spacy
from spacy import displacy
import requests
import utils
from utils import is_blacklisted
from streamlit_timeline import timeline
import data_manager as dm
from data_manager import get_timeline_events

# 1. PAGE SETUP (Must be the very first command)
st.set_page_config(page_title="Bible Study Partner", layout="wide")


# --- 2. AI SETUP ---
@st.cache_resource
def load_nlp():
    nlp = spacy.load("en_core_web_sm")
    if "entity_ruler" not in nlp.pipe_names:
        config = {"overwrite_ents": True}
        ruler = nlp.add_pipe("entity_ruler", before="ner", config=config)
        base_patterns = utils.get_base_patterns()
        ruler.add_patterns(base_patterns)
    return nlp


nlp = load_nlp()


# --- 3. DATA FUNCTIONS ---
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        return response.json()['text'] if response.status_code == 200 else None
    except:
        return None


def get_fallback_timeline(reference):
    db = {
        "John": [{"Event": "Birth of Jesus", "Date": -4}, {"Event": "Crucifixion", "Date": 30}],
        "Genesis": [{"Event": "Creation", "Date": -4004}, {"Event": "The Flood", "Date": -2348}]
    }
    book = reference.split()[0].title()
    return db.get(book, [])

# --- 1. INITIALIZATION ---
if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

# --- 2. SIDEBAR NAVIGATION & SELECTION ---
st.sidebar.header("Navigation")
book = st.sidebar.selectbox("Choose a Book", list(dm.BIBLE_CHAPTER_COUNTS.keys()))
chapter = st.sidebar.number_input("Chapter", 1, dm.BIBLE_CHAPTER_COUNTS[book], value=1)

# Combined Reset & Home
if st.sidebar.button("🏠 Home / Reset"):
    st.session_state.run_analysis = False
    st.rerun()

# --- 3. STUDY SETTINGS ---
st.sidebar.divider()
st.sidebar.header("Study Settings")
ref = st.sidebar.text_input("Reference:", "Genesis 1:1")
show_stats = st.sidebar.checkbox("Show Stats", value=True)

versions = {"World English Bible": "web", "King James Version": "kjv"}
v_choice = st.sidebar.selectbox("Version:", list(versions.keys()))
translation_code = versions[v_choice]

if st.sidebar.button("🔍 Analyze Scripture"):
    st.session_state.run_analysis = True

# --- 4. EXTERNAL RESOURCES ---
st.sidebar.divider()
st.sidebar.subheader("📚 Study Resources")
gq_url = dm.get_gotquestions_url(book, chapter)
st.sidebar.link_button(f"Study {book} {chapter} on GotQuestions", gq_url)

# --- 5. VISUALIZATION CONFIG ---
options = {
    "ents": ["GOD", "PERSON", "PEOPLE GROUPS", "GPE", "tøp"],
    "colors": {"GOD": "purple", "PERSON": "#4facfe", "PEOPLE GROUPS": "orange", "GPE": "#98FB98", "tøp": "red"}
}


# --- 6. PAGE RENDERING ---

# CASE A: THE WELCOME PAGE
if not st.session_state.run_analysis:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');

            :root { 
                --bandito-yellow: #FCE300; 
                --deep-grey: #212121; 
            }

            /* Main Background and Font */
            .stApp { 
                background-color: var(--deep-grey); 
                color: white; 
                font-family: 'Courier Prime', monospace;
            }

            /* Bandito Glitch Effect for Titles */
            h1, h2, h3 { 
                color: var(--bandito-yellow) !important; 
                text-transform: uppercase;
                letter-spacing: 2px;
                position: relative;
                animation: glitch 3s infinite;
            }

            @keyframes glitch {
                0% { text-shadow: 2px 0 red, -2px 0 cyan; }
                2% { text-shadow: 5px 0 red, -5px 0 cyan; }
                4% { text-shadow: 2px 0 red, -2px 0 cyan; }
                100% { text-shadow: 2px 0 red, -2px 0 cyan; }
            }

            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #1a1a1a;
                border-right: 1px solid var(--bandito-yellow);
            }

            /* Button Styling */
            .stButton>button { 
                background-color: var(--bandito-yellow); 
                color: black; 
                font-weight: bold; 
                border-radius: 0px;
                border: 2px solid black;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: black;
                color: var(--bandito-yellow);
                border: 2px solid var(--bandito-yellow);
            }

            /* Scripture Container */
            .bible-container { 
                border-left: 5px solid var(--bandito-yellow); 
                padding: 20px; 
                background-color: #121212; 
                border-radius: 0px; 
                line-height: 1.6;
            }
            
            /* Metric Label Styling (The titles like 'Divine', 'People') */
            [data-testid="stMetricLabel"] {
                color: var(--bandito-yellow) !important;
                font-family: 'Courier Prime', monospace !important;
                text-transform: uppercase;
            }
            
            /* Metric Value Styling (The actual numbers) */
            [data-testid="stMetricValue"] {
                color: white !important;
                text-shadow: 1px 1px 5px var(--bandito-yellow); /* Gives it a slight glow */
            }
            
            </style>

            ### Welcome to the Trench Study 📖
            This AI tool helps you navigate the layers of Scripture.

            **Mission Protocol:**
            1. Initialize reference in sidebar.
            2. Choose translation version.
            3. Deploy **'Analyze Scripture'**.
        """, unsafe_allow_html=True)
        st.info("💡 **Status:** Historical Timelines active for Genesis. Stay low.")

    with col2:
        try:
            st.image("welcome_torch.jpg", use_container_width=True)
        except:
            st.image("https://images.unsplash.com/photo-1504052434569-70ad5836ab65?q=80&w=1000")
        st.markdown(
            "<div style='text-align: center; color: #FCE300; font-family: monospace;'>‖—‖ keep your torch lit ‖—‖</div>",
            unsafe_allow_html=True)

    # --- B. THE ANALYSIS PAGE ---
else:
    raw_text = get_bible_text(ref, trans=translation_code)

    if raw_text:
        parts = ref.split()
        book_name = parts[0].title()
        # Clean chapter extraction
        chapter_num = parts[1].split(':')[0] if len(parts) > 1 else "All"

        # --- 1. TIMELINE LOGIC ---
        # We unpack BOTH the list and the pre-calculated index from your data_manager
        events, start_index = get_timeline_events(book_name, chapter_num)

        if events:
            # Create the data package for the timeline component
            timeline_data = {
                "events": events,
                "start_at_slide": start_index  # This now uses the unpacked value
            }

            st.subheader(f"⏳ {book_name}: Chapter {chapter_num} Intelligence")
            timeline(timeline_data, height=600)

        else:
            # Fallback to "All" if specific chapter has no events
            # Note: We unpack here as well to keep the return types consistent
            all_events, all_start_index = get_timeline_events(book_name, "All")

            if all_events:
                st.info(f"Showing full historical intel for {book_name}")
                timeline({"events": all_events, "start_at_slide": all_start_index}, height=600)
            else:
                st.warning(f"No timeline data found for {book_name}. Proceeding to text analysis.")

        # --- 2. TEXT HIGHLIGHTING SECTION (Now properly indented) ---
        st.divider()
        st.subheader(f"📖 Scripture Analysis: {ref}")

        doc = nlp(raw_text)
        doc.ents = [e for e in doc.ents if not is_blacklisted(e.text) and e.label_ in options["ents"]]

        if show_stats:
            counts = doc.count_by(spacy.attrs.IDS['ENT_TYPE'])
            cols = st.columns(5)


            def gc(label):
                return counts.get(nlp.vocab.strings[label], 0) if label in nlp.vocab.strings else 0


            cols[0].metric("Divine", gc("GOD"))
            cols[1].metric("People", gc("PERSON"))
            cols[2].metric("Groups", gc("PEOPLE GROUPS"))
            cols[3].metric("Places", gc("GPE"))
            cols[4].metric("tøp", gc("tøp"))

        # Render highlighted Bible text
        html = displacy.render(doc, style="ent", options=options)
        st.markdown(f"<div class='bible-container'>{html}</div>", unsafe_allow_html=True)

        st.write("")
        if st.button("← Back to Welcome Page"):
            st.session_state.run_analysis = False
            st.rerun()

    else:
        st.error(f"Reference '{ref}' not found. Please try again.")
        if st.button("Back Home"):
            st.session_state.run_analysis = False
            st.rerun()

import streamlit as st
import data_manager as dm
import random

# --- PAGE SETUP ---
st.set_page_config(page_title="Bible Game Center", page_icon="📖")
st.title("📖 Bible Game Center")

# --- INITIALIZE GLOBAL STATE ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'game_over' not in st.session_state: st.session_state.game_over = False

# --- SIDEBAR: NAVIGATION ---
st.sidebar.header("Settings")
book = st.sidebar.selectbox("Book", list(dm.BIBLE_CHAPTER_COUNTS.keys()))
max_chaps = dm.BIBLE_CHAPTER_COUNTS[book]
chapter = st.sidebar.number_input("Chapter", 1, max_chaps, value=1, key = "sidebar_chapter_selector")

if st.sidebar.button("Reset All Games"):
    for key in ['score', 'current_q', 'game_over', 'hangman_word', 'guessed_letters']:
        if key in st.session_state: del st.session_state[key]
    st.rerun()

tab1, tab2 = st.tabs(["📝 Trivia", "🔤 Hangman"])

# --- TAB 1: TRIVIA ---
with tab1:
    # 1. Try to get manual trivia first
    questions = dm.get_trivia_questions(book, chapter)

    # 2. FALLBACK: If no manual trivia, generate it!
    if not questions:
        st.info("No manual trivia found. Generating automatic questions...")
        questions = dm.get_auto_trivia(book, chapter)
    if questions and not st.session_state.game_over:
        q = questions[st.session_state.current_q]
        st.subheader(f"Question {st.session_state.current_q + 1}")
        st.write(f"### {q['question']}")

        with st.form("trivia_form"):
            choice = st.radio("Answer:", q['options'])
            if st.form_submit_button("Submit"):
                if choice == q['answer']:
                    st.success(f"Correct! {q.get('reference', '')}")
                    st.session_state.score += 1
                else:
                    st.error(f"Wrong! Answer: {q['answer']}")

                if st.session_state.current_q + 1 < len(questions):
                    st.session_state.current_q += 1
                else:
                    st.session_state.game_over = True
                st.button("Continue")

    elif st.session_state.game_over:
        st.success(f"Finished! Score: {st.session_state.score}/{len(questions)}")
    else:
        st.info("No manual trivia found. Use Hangman for auto-generation!")

# --- TAB 2: HANGMAN ---
with tab2:
    # 1. Generation Logic
    if st.button("Generate New Word from Chapter"):
        data = dm.generate_auto_game(book, chapter)
        if data and data['game_words']:
            st.session_state.hangman_word = random.choice(data['game_words'])
            st.session_state.guessed_letters = []
            st.session_state.attempts_left = 6
            st.rerun()

    # 2. Display Logic (Fixed: Outside the button so it persists)
    if 'hangman_word' in st.session_state:
        word = st.session_state.hangman_word
        guesses = st.session_state.guessed_letters

        display = [l if l in guesses else "_" for l in word]
        st.subheader(" ".join(display))

        col1, col2 = st.columns([2, 1])
        with col1:
            char = st.text_input("Guess a letter:", max_chars=1, key="input").upper()
        with col2:
            if st.button("Guess") and char:
                if char not in guesses:
                    guesses.append(char)
                    if char not in word: st.session_state.attempts_left -= 1
                st.rerun()

        st.write(f"Lives: {'❤️' * st.session_state.attempts_left} | Guessed: {', '.join(guesses)}")

        if "_" not in display:
            st.balloons();
            st.success(f"You won! Word: {word}")
        elif st.session_state.attempts_left <= 0:
            st.error(f"Game Over! Word: {word}")


