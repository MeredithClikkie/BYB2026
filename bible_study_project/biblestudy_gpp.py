import streamlit as st
import requests
import spacy
import random
import re
from streamlit_timeline import timeline
import data_manager as dm

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Bible Study Partner", layout="wide", page_icon="📖")


# --- 2. AI & NLP SETUP ---
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")


nlp = load_nlp()

# --- 3. SESSION STATE INITIALIZATION ---
if "run_analysis" not in st.session_state: st.session_state.run_analysis = False
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'game_over' not in st.session_state: st.session_state.game_over = False

# --- 4. SIDEBAR NAVIGATION (The Master Controller) ---
st.sidebar.header("📡 Mission Briefing")

# A. Mission Sync Logic
plan_options = list(dm.READING_PLANS.keys())
plan_choice = st.sidebar.selectbox("Active Plan", plan_options)
day_num = st.sidebar.number_input("Mission Day", 1, 365, value=1)

if st.sidebar.button("🎯 Sync to Today's Reading"):
    mission = dm.READING_PLANS[plan_choice].get(day_num)
    if mission:
        st.session_state.book_choice = mission['book']
        st.session_state.chap_choice = mission['chap']
        st.rerun()

st.sidebar.divider()

# B. Smart Selection
default_book = st.session_state.get('book_choice', 'Genesis')
book_list = list(dm.BIBLE_CHAPTER_COUNTS.keys())
book_index = book_list.index(default_book) if default_book in book_list else 0

book = st.sidebar.selectbox("Current Book", book_list, index=book_index)

max_chaps = dm.BIBLE_CHAPTER_COUNTS[book]
default_chap = st.session_state.get('chap_choice', 1)
safe_chap = default_chap if default_chap <= max_chaps else 1

chapter = st.sidebar.number_input("Chapter", 1, max_chaps, value=safe_chap, key="master_chap")

# C. Home / Reset
if st.sidebar.button("🏠 Home / Reset"):
    st.session_state.run_analysis = False
    if 'book_choice' in st.session_state: del st.session_state.book_choice
    if 'chap_choice' in st.session_state: del st.session_state.chap_choice
    st.rerun()

st.sidebar.divider()
st.sidebar.header("Study Settings")

# D. SMART PARSER: Syncs typed text BACK to the timeline variables
ref = st.sidebar.text_input("Analysis Reference:", value=f"{book} {chapter}", key="ref_input")

if ref != f"{book} {chapter}":
    match = re.match(r"(.+?)\s+(\d+)", ref)
    if match:
        new_book, new_chap = match.group(1).strip(), int(match.group(2))
        if new_book in book_list:
            st.session_state.book_choice, st.session_state.chap_choice = new_book, new_chap
            st.rerun()

        # E. Study Hub Configs
versions = {"World English Bible": "web", "King James Version": "kjv"}
v_choice = st.sidebar.selectbox("Version:", list(versions.keys()), key="sidebar_v_selector")
translation_code = versions[v_choice]
show_stats = st.sidebar.checkbox("Show AI Stats", value=True, key="sidebar_stats_cb")

if st.sidebar.button("🔍 Analyze Mission Scripture", key="deploy_mission_btn"):
    st.session_state.run_analysis = True
    st.rerun()

if st.sidebar.button("💎 Ned's Insight"):
    proverbs = ["Proverbs 3:5", "Proverbs 16:3", "Proverbs 18:10"]
    st.toast(f"Ned says: Check out {random.choice(proverbs)}!", icon="✨")

options = {
    "ents": ["GOD", "PERSON", "PEOPLE GROUPS", "GPE", "tøp"],
    "colors": {"GOD": "purple", "PERSON": "#4facfe", "PEOPLE GROUPS": "orange", "GPE": "#98FB98", "tøp": "red"}
}

# --- 5. PAGE RENDERING ---

# CASE A: THE WELCOME PAGE
if not st.session_state.run_analysis:
    st.markdown("""<style>.stApp { background-color: #212121; color: white; font-family: monospace; }
        h1, h2, h3 { color: #FCE300 !important; text-transform: uppercase; }</style>""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Welcome to the Trench Study 📖\nThis AI tool helps you navigate the layers of Scripture.")
        st.info("💡 **Status:** Historical Timelines active. Stay low.")
    with col2:
        st.image("https://images.unsplash.com/photo-1504052434569-70ad5836ab65?q=80&w=1000")
        st.markdown("<div style='text-align: center; color: #FCE300;'>‖—‖ keep your torch lit ‖—‖</div>",
                    unsafe_allow_html=True)

    st.divider()
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Trivia", "🔤 Hangman", "📚 Resources", "📓 Journal"])

    with tab1:  # TRIVIA
        questions = dm.get_trivia_questions(book, chapter)
        if not questions: questions = dm.get_auto_trivia(book, chapter)
        if questions and not st.session_state.game_over:
            q = questions[st.session_state.current_q]
            with st.form("trivia_form"):
                choice = st.radio(f"Question {st.session_state.current_q + 1}: {q['question']}", q['options'])
                if st.form_submit_button("Submit Answer"):
                    if choice == q['answer']:
                        st.success("Correct!")
                    else:
                        st.error(f"Wrong! Answer: {q['answer']}")
                    st.session_state.current_q = (
                                st.session_state.current_q + 1) if st.session_state.current_q + 1 < len(
                        questions) else st.session_state.current_q
                    if st.session_state.current_q + 1 == len(questions): st.session_state.game_over = True
            if st.button("Continue"): st.rerun()

    with tab2:  # HANGMAN
        if st.button("Generate New Word"):
            data = dm.generate_auto_game(book, chapter)
            if data: st.session_state.hangman_word = random.choice(data['game_words'])
            st.rerun()

    with tab3:  # RESOURCES
        st.header(f"Study Hub: {book} {chapter}")
        st.link_button("Bible Hub Interlinear", f"https://biblehub.com/{book.lower().replace(' ', '_')}/{chapter}.htm",
                       use_container_width=True)
        show_audio = st.toggle("Enable Lofi Study Beats")
        if show_audio: st.video("https://www.youtube.com/watch?v=qXPoj_VYb3U")

    with tab4:  # JOURNAL & PROGRESS
        st.header("📓 Mission Progress & Journal")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cols = st.columns(7)
        for i, d in enumerate(days):
            cols[i].checkbox(d, key=f"mission_{d}")

        st.divider()
        st.subheader("📝 LASB Notes (SOAP)")
        col_l, col_r = st.columns(2)
        with col_l:
            s_n = st.text_area("📖 Scripture (S)", placeholder=dm.LASB_PROMPTS['S'], key=f"S_{book}_{chapter}")
            a_n = st.text_area("💡 Application (A)", placeholder=dm.LASB_PROMPTS['A'], key=f"A_{book}_{chapter}")
        with col_r:
            o_n = st.text_area("🧐 Observation (O)", placeholder=dm.LASB_PROMPTS['O'], key=f"O_{book}_{chapter}")
            p_n = st.text_area("🙏 Prayer (P)", placeholder=dm.LASB_PROMPTS['P'], key=f"P_{book}_{chapter}")
        if st.button("💾 Archive Notes"): st.success("Notes archived in Trench Logs.")

# CASE B: THE ANALYSIS PAGE
else:
    raw_text = dm.get_bible_text(ref, trans=translation_code)
    if raw_text:
        events, start_index = dm.get_timeline_events(book, chapter)
        if events:
            st.subheader(f"⏳ {book} Intelligence Timeline")
            timeline({"events": events, "start_at_slide": start_index}, height=500)

        st.divider()
        st.subheader(f"📖 AI Analysis: {ref}")
        doc = nlp(raw_text)
        if show_stats:
            c1, c2 = st.columns(2)
            c1.metric("Characters", len([e for e in doc.ents if e.label_ == "PERSON"]))
            c2.metric("Locations", len([e for e in doc.ents if e.label_ == "GPE"]))

        import spacy.displacy as displacy

        html = displacy.render(doc, style="ent", options=options)
        st.markdown(f"<div class='bible-container'>{html}</div>", unsafe_allow_html=True)

        if st.button("← Back to Mission Command"):
            st.session_state.run_analysis = False
            st.rerun()