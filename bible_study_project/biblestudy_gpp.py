import streamlit as st
import requests
import spacy
import random
import re
from streamlit_timeline import timeline
import data_manager as dm  # Ensure your data_manager.py is in the same folder

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Bible Study Partner", layout="wide", page_icon="📖")


# --- 2. AI & NLP SETUP ---
@st.cache_resource
def load_nlp():
    nlp = spacy.load("en_core_web_sm")
    # Add custom entity ruler logic here if needed from your utils
    return nlp


nlp = load_nlp()


# --- 3. CORE FUNCTIONS ---
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        return response.json()['text'] if response.status_code == 200 else None
    except:
        return None


# --- 4. SESSION STATE INITIALIZATION ---
if "run_analysis" not in st.session_state: st.session_state.run_analysis = False
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'game_over' not in st.session_state: st.session_state.game_over = False

# --- 5. SIDEBAR NAVIGATION (The Master Controller) ---
st.sidebar.header("Navigation")
book = st.sidebar.selectbox("Choose a Book", list(dm.BIBLE_CHAPTER_COUNTS.keys()))
max_chaps = dm.BIBLE_CHAPTER_COUNTS[book]
chapter = st.sidebar.number_input("Chapter", 1, max_chaps, value=1, key="sidebar_chapter_selector")

if st.sidebar.button("🏠 Home / Reset"):
    st.session_state.run_analysis = False
    st.session_state.game_over = False
    st.rerun()

st.sidebar.divider()
st.sidebar.header("Study Settings")
# Dynamic default reference based on selection
default_ref = f"{book} {chapter}"
ref = st.sidebar.text_input("Analysis Reference:", value=default_ref)

versions = {"World English Bible": "web", "King James Version": "kjv"}
v_choice = st.sidebar.selectbox("Version:", list(versions.keys()))
translation_code = versions[v_choice]
show_stats = st.sidebar.checkbox("Show AI Stats", value=True)

if st.sidebar.button("🔍 Analyze Scripture"):
    st.session_state.run_analysis = True

if st.sidebar.button("💎 Ned's Insight"):
    proverbs = ["Proverbs 3:5", "Proverbs 16:3", "Proverbs 18:10"]
    st.toast(f"Ned says: Check out {random.choice(proverbs)}!", icon="✨")

# Visual Config for NLP
options = {
    "ents": ["GOD", "PERSON", "PEOPLE GROUPS", "GPE", "tøp"],
    "colors": {"GOD": "purple", "PERSON": "#4facfe", "PEOPLE GROUPS": "orange", "GPE": "#98FB98", "tøp": "red"}
}

# --- 6. PAGE RENDERING ---

# CASE A: THE WELCOME & GAME HUB
if not st.session_state.run_analysis:
    st.title("📖 Bible Trench Study & Game Center")

    # CSS for the "Bandito" Glitch Aesthetic
    st.markdown("""
        <style>
        .stApp { background-color: #212121; color: white; font-family: monospace; }
        h1, h2, h3 { color: #FCE300 !important; text-transform: uppercase; }
        .bible-container { border-left: 5px solid #FCE300; padding: 20px; background-color: #121212; }
        </style>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📝 Trivia", "🔤 Hangman", "📚 Resources", "📓 Journal"])

    with tab1:  # TRIVIA
        questions = dm.get_trivia_questions(book, chapter)
        if not questions:
            st.info("Generating automatic questions...")
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
            if st.button("Restart Trivia"):
                st.session_state.game_over = False
                st.session_state.score = 0
                st.session_state.current_q = 0
                st.rerun()

    with tab2:  # HANGMAN
        if st.button("Generate New Word from Chapter"):
            data = dm.generate_auto_game(book, chapter)
            if data and data['game_words']:
                st.session_state.hangman_word = random.choice(data['game_words'])
                st.session_state.guessed_letters = []
                st.session_state.attempts_left = 6
                st.rerun()

        if 'hangman_word' in st.session_state:
            word = st.session_state.hangman_word
            display = [l if l in st.session_state.guessed_letters else "_" for l in word]
            st.subheader(" ".join(display))
            char = st.text_input("Guess a letter:", max_chars=1, key="hg_input").upper()
            if st.button("Submit Guess") and char:
                if char not in st.session_state.guessed_letters:
                    st.session_state.guessed_letters.append(char)
                    if char not in word: st.session_state.attempts_left -= 1
                st.rerun()
            st.write(f"Lives: {'❤️' * st.session_state.attempts_left}")

    with tab3:  # RESOURCES
        st.header(f"Study Hub: {book} {chapter}")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Textual Resources")
            st.link_button("GotQuestions Overview", dm.get_gotquestions_url(book, chapter), use_container_width=True)
            bh_url = f"https://biblehub.com/{book.lower().replace(' ', '_')}/{chapter}.htm"
            st.link_button("Bible Hub Interlinear", bh_url, use_container_width=True)
        with col2:
            st.subheader("Visual Overview")
            bp_url = dm.get_bible_project_url(book)
            if bp_url:
                st.video(bp_url)
                st.caption("Video not loading? [Watch on YouTube](" + bp_url.replace("embed/", "watch?v=") + ")")

    with tab3:
        st.divider()
        st.subheader("🎧 Atmosphere: Lofi Study Beats")

        # Toggle for the music so it doesn't play automatically
        show_audio = st.toggle("Enable Background Study Music")

        if show_audio:
            # Using a reliable 24/7 Christian Lofi stream
            lofi_url = "https://www.youtube.com/watch?v=qXPoj_VYb3U"

            # We use st.video here because it handles YouTube live streams better than st.audio
            # Setting the height small keeps it discreet
            st.video(lofi_url)
            st.caption("Now Playing: 24/7 Christian Lofi Radio")
        else:
            st.info("Switch the toggle above to play instrumental study beats.")


    # --- TAB 4: JOURNAL & PROGRESS ---
    with tab4: # JOURNAL
        st.header("📓 Study Journal")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Progress Tracker")
            # List of all 66 books for the checklist
            all_books = list(dm.BIBLE_CHAPTER_COUNTS.keys())

            # This multiselect acts as your 'Check off' list
            read_books = st.multiselect(
                "Which books have you completed?",
                options=all_books,
                default=st.session_state.get("completed_books", []),
                key="progress_tracker"
            )
            st.session_state.completed_books = read_books

            # Calculate percentage
            percent = round((len(read_books) / 66) * 100, 1)
            st.progress(len(read_books) / 66)
            st.write(f"You have completed **{percent}%** of the Bible!")

        with col2:
            st.subheader("Daily Prompt")
            # Get specific prompt for the book, or use the default
            prompt = dm.JOURNAL_PROMPTS.get(book, dm.DEFAULT_PROMPT)
            st.info(f"**Reflect on {book}:**\n\n{prompt}")

        st.divider()
        # Inside your Journal Tab (tab4)
        st.subheader("📝 Life Application Study Notes (SOAP)")

        col_s, col_o = st.columns(2)
        with col_s:
            st.text_area("📖 Scripture", placeholder="Copy the verse that stood out...", key=f"soap_s_{book}_{chapter}")
        with col_o:
            st.text_area("🧐 Observation", placeholder="What is happening in this text?", key=f"soap_o_{book}_{chapter}")

        col_a, col_p = st.columns(2)
        with col_a:
            st.text_area("💡 Application", placeholder="How does this change my life today?",
                         key=f"soap_a_{book}_{chapter}")
        with col_p:
            st.text_area("🙏 Prayer", placeholder="Write a short prayer regarding this text...",
                         key=f"soap_p_{book}_{chapter}")


# CASE B: THE ANALYSIS PAGE
else:
    raw_text = get_bible_text(ref, trans=translation_code)
    if raw_text:
        # TIMELINE
        events, start_index = dm.get_timeline_events(book, chapter)
        if events:
            st.subheader(f"⏳ {book} Intelligence Timeline")
            timeline({"events": events, "start_at_slide": start_index}, height=500)

        # SCRIPTURE HIGHLIGHTING
        st.divider()
        st.subheader(f"📖 AI Analysis: {ref}")
        doc = nlp(raw_text)
        # (Filtering logic for entities would go here)

        if show_stats:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Divine References", "Analysis Active")  # Simplified for condensation

        import spacy.displacy as displacy

        html = displacy.render(doc, style="ent", options=options)
        st.markdown(f"<div class='bible-container'>{html}</div>", unsafe_allow_html=True)

        if st.button("← Back to Menu"):
            st.session_state.run_analysis = False
            st.rerun()
    else:
        st.error("Reference not found.")