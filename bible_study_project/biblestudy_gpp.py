import streamlit as st
import spacy
import random
import re
from streamlit_timeline import timeline
import data_manager as dm

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Trench Study AI", layout="wide", page_icon="📖")

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
if 'book_choice' not in st.session_state: st.session_state.book_choice = 'Genesis'
if 'chap_choice' not in st.session_state: st.session_state.chap_choice = 1

# --- 4. GLOBAL STATE SYNC (The Master variables) ---
book_list = list(dm.BIBLE_CHAPTER_COUNTS.keys())
book = st.session_state.book_choice
chapter = st.session_state.chap_choice

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.header("📡 Mission Briefing")

# A. Single Command Option (Target Reference)
ref = st.sidebar.text_input("🎯 Target Reference:", value=f"{book} {chapter}", key="ref_input")

# Smart Sync Logic: Updates state immediately if you type a new reference
if ref != f"{book} {chapter}":
    match = re.match(r"(.+?)\s+(\d+)", ref)
    if match:
        p_book = match.group(1).strip()
        p_chap = int(match.group(2))
        if p_book in book_list:
            st.session_state.book_choice = p_book
            st.session_state.chap_choice = p_chap
            st.rerun()

st.sidebar.divider()

# B. Tactical Override & Plans (Expandable)
with st.sidebar.expander("🛠️ Manual Overrides & Plans"):
    b_idx = book_list.index(book) if book in book_list else 0
    m_book = st.selectbox("Manual Book Select", book_list, index=b_idx, key="manual_sel")
    if m_book != book:
        st.session_state.book_choice = m_book
        st.rerun()

    st.subheader("Mission Plans")
    plan_choice = st.selectbox("Active Plan", list(dm.READING_PLANS.keys()))
    day_num = st.number_input("Mission Day", 1, 365, value=1)
    if st.button("🎯 Sync Plan"):
        mission = dm.READING_PLANS[plan_choice].get(day_num)
        if mission:
            st.session_state.book_choice = mission['book']
            st.session_state.chap_choice = mission['chap']
            st.rerun()

st.sidebar.header("Study Settings")
versions = {"World English Bible": "web", "King James Version": "kjv"}
v_choice = st.sidebar.selectbox("Version:", list(versions.keys()))
translation_code = versions[v_choice]
show_stats = st.sidebar.checkbox("Show AI Stats", value=True)

# C. Deployment & Reset Buttons
col_a, col_b = st.sidebar.columns(2)
if col_a.button("🔍 Analyze"):
    st.session_state.run_analysis = True
    st.rerun()

if col_b.button("🏠 Home"):
    st.session_state.run_analysis = False
    st.rerun()

if st.sidebar.button("💎 Ned's Insight"):
    proverbs = ["Proverbs 3:5", "Proverbs 16:3", "Proverbs 18:10"]
    st.toast(f"Ned says: Check out {random.choice(proverbs)}!", icon="✨")

options = {
    "ents": ["GOD", "PERSON", "PEOPLE GROUPS", "GPE", "tøp"],
    "colors": {"GOD": "purple", "PERSON": "#4facfe", "PEOPLE GROUPS": "orange", "GPE": "#98FB98", "tøp": "red"}
}

# --- 6. PAGE RENDERING ---

# CASE A: THE WELCOME PAGE
if not st.session_state.run_analysis:
    st.markdown("""<style>.stApp { background-color: #212121; color: white; font-family: monospace; }
        h1, h2, h3 { color: #FCE300 !important; text-transform: uppercase; }</style>""", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"### Welcome to the Trench Study 📖")
        st.info(f"💡 **Current Intel:** Ready to analyze {book} {chapter}.")
    with c2:
        st.image("https://images.unsplash.com/photo-1504052434569-70ad5836ab65?q=80&w=1000")
        st.markdown("<div style='text-align: center; color: #FCE300;'>‖—‖ keep your torch lit ‖—‖</div>", unsafe_allow_html=True)

    st.divider()
    t1, t2, t3, t4 = st.tabs(["📝 Trivia", "🔤 Hangman", "📚 Resources", "📓 Journal"])

    with t1:
        questions = dm.get_trivia_questions(book, chapter)
        if not questions: questions = dm.get_auto_trivia(book, chapter)
        if questions and not st.session_state.game_over:
            q = questions[st.session_state.current_q]
            with st.form("trivia_form"):
                choice = st.radio(f"Question: {q['question']}", q['options'])
                if st.form_submit_button("Submit Answer"):
                    if choice == q['answer']: st.success("Correct!")
                    else: st.error(f"Wrong! Answer: {q['answer']}")
                    st.session_state.current_q = (st.session_state.current_q + 1) if st.session_state.current_q + 1 < len(questions) else st.session_state.current_q
                    if st.session_state.current_q + 1 == len(questions): st.session_state.game_over = True
            if st.button("Continue"): st.rerun()

    with t2:
        if st.button("Generate Word"):
            data = dm.generate_auto_game(book, chapter)
            if data: st.session_state.hangman_word = random.choice(data['game_words'])
            st.rerun()

    with t3:
        st.header(f"Study Hub: {book} {chapter}")
        st.link_button("Bible Hub Interlinear", f"https://biblehub.com/{book.lower().replace(' ', '_')}/{chapter}.htm")
        if st.toggle("Enable Lofi Study Beats"): st.video("https://www.youtube.com/watch?v=qXPoj_VYb3U")

    with t4:
        st.header("📓 Journal")
        c_l, c_r = st.columns(2)
        with c_l:
            st.text_area("📖 Scripture (S)", placeholder=dm.LASB_PROMPTS['S'], key=f"S_{book}_{chapter}")
        with c_r:
            st.text_area("🧐 Observation (O)", placeholder=dm.LASB_PROMPTS['O'], key=f"O_{book}_{chapter}")

# CASE B: THE ANALYSIS PAGE
else:
    # 1. FORCE THE SYNC: Re-parse the text box right now
    import re

    match = re.match(r"(.+?)\s+(\d+)", ref)
    if match:
        current_book = match.group(1).strip()
        current_chap = int(match.group(2))
    else:
        # Fallback to session state if regex fails
        current_book = book
        current_chap = chapter

    # 2. FETCH TEXT (Using the raw 'ref' from sidebar)
    raw_text = dm.get_bible_text(ref, trans=translation_code)

    if raw_text:
        # 3. FETCH TIMELINE (Using the forced variables)
        events, start_index = dm.get_timeline_events(current_book, current_chap)

        # 4. RENDER TIMELINE FIRST
        if events:
            st.subheader(f"⏳ {current_book} {current_chap} Intelligence Timeline")
            # We wrap it in a container to ensure it renders cleanly
            with st.container():
                timeline({"events": events, "start_at_slide": start_index}, height=450)
        else:
            st.warning("No specific historical intel found for this sector, but staying alert.")

        # 5. RENDER SCRIPTURE & AI ANALYSIS
        st.divider()
        st.subheader(f"📖 AI Analysis: {ref}")

        # NLP Processing
        doc = nlp(raw_text)

        if show_stats:
            m1, m2 = st.columns(2)
            m1.metric("Characters", len([e for e in doc.ents if e.label_ == "PERSON"]))
            m2.metric("Locations", len([e for e in doc.ents if e.label_ == "GPE"]))

        # Displacy Highlighting
        import spacy.displacy as displacy

        html = displacy.render(doc, style="ent", options=options)

        # The CSS ensures the text is readable and themed
        st.markdown(f"<div style='color: white; background: #2d2d2d; padding: 20px; border-radius: 10px;'>{html}</div>",
                    unsafe_allow_html=True)

        if st.button("← Back to Mission Command"):
            st.session_state.run_analysis = False
            st.rerun()
