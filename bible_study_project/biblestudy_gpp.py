import streamlit as st
import spacy
import random
import re
import requests
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
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'game_over' not in st.session_state: st.session_state.game_over = False
if 'book_choice' not in st.session_state: st.session_state.book_choice = 'Genesis'
if 'chap_choice' not in st.session_state: st.session_state.chap_choice = 1

# --- 4. GLOBAL STATE SYNC ---
book_list = list(dm.BIBLE_CHAPTER_COUNTS.keys())
book = st.session_state.book_choice
chapter = st.session_state.chap_choice


# --- 5. HELPER FUNCTIONS ---
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        r = requests.get(url)
        return r.json()['text'] if r.status_code == 200 else "Text not found."
    except Exception as e:
        return f"Connection error: {str(e)}"


# --- 6. SIDEBAR NAVIGATION ---
st.sidebar.header("📡 Mission Briefing")
ref = st.sidebar.text_input("🎯 Target Reference:", value=f"{book} {chapter}", key="ref_input")

# Smart Sync Logic: Updates state immediately if you type a new reference
if ref != f"{book} {chapter}":
    match = re.match(r"(.+?)\s+(\d+)", ref)
    if match:
        p_book = match.group(1).strip().title()
        p_chap = int(match.group(2))
        if p_book in book_list:
            st.session_state.book_choice = p_book
            st.session_state.chap_choice = p_chap
            st.rerun()

with st.sidebar.expander("🛠️ Manual Overrides & Plans"):
    b_idx = book_list.index(book) if book in book_list else 0
    m_book = st.selectbox("Manual Book Select", book_list, index=b_idx)
    if m_book != book:
        st.session_state.book_choice = m_book
        st.rerun()

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

col_a, col_b = st.sidebar.columns(2)
if col_a.button("🔍 Analyze"):
    st.session_state.run_analysis = True
    st.rerun()
if col_b.button("🏠 Home"):
    st.session_state.run_analysis = False
    st.rerun()

# --- 7. PAGE RENDERING ---

# CASE A: THE WELCOME PAGE
if not st.session_state.run_analysis:
    st.markdown("""<style>.stApp { background-color: #212121; color: white; font-family: monospace; }
        h1, h2, h3 { color: #FCE300 !important; text-transform: uppercase; }</style>""", unsafe_allow_html=True)

    st.markdown(f"### Welcome to the Trench Study 📖")
    st.info(f"💡 **Current Intel:** Ready to analyze {book} {chapter}.")

    t1, t2, t3, t4 = st.tabs(["📝 Trivia", "📚 Resources", "📓 Journal", "🎥 Video"])

    with t1:
        questions = dm.get_trivia_questions(book, chapter)
        if not questions: questions = dm.get_auto_trivia(book, chapter)
        if questions:
            q = questions[st.session_state.current_q % len(questions)]
            st.write(f"**Question:** {q['question']}")
            ans = st.radio("Options:", q['options'], key="trivia_radio")
            if st.button("Submit Answer"):
                if ans == q['answer']:
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The answer is {q['answer']}")

    with t2:
        st.link_button("Bible Hub Interlinear", f"https://biblehub.com/{book.lower().replace(' ', '_')}/{chapter}.htm")

    with t3:
        st.text_area("📖 Scripture (S)", placeholder=dm.LASB_PROMPTS['S'])
        st.text_area("🧐 Observation (O)", placeholder=dm.LASB_PROMPTS['O'])

    with t4:
        # Pulls from your BP_MAP in data_manager
        v_id = dm.BP_MAP.get(book)
        if v_id:
            st.video(f"https://www.youtube.com/watch?v={v_id}")

# CASE B: THE ANALYSIS PAGE
else:
    # 1. FETCH CONTENT
    raw_text = get_bible_text(ref, trans=translation_code)

    if raw_text:
        # 2. FETCH TIMELINE (dm.get_timeline_events handles Acts/Letters logic)
        events, start_index = dm.get_timeline_events(book, chapter)

        st.subheader(f"📖 {ref}")

        # 3. RENDER TIMELINE
        if events:
            timeline({"events": events, "start_at_slide": start_index}, height=450)

        # 4. RENDER TEXT & AI ANALYSIS
        st.divider()
        doc = nlp(raw_text)

        if show_stats:
            m1, m2 = st.columns(2)
            m1.metric("Characters Found", len([e for e in doc.ents if e.label_ == "PERSON"]))
            m2.metric("Locations Found", len([e for e in doc.ents if e.label_ == "GPE"]))

        # Displacy Highlighting
        import spacy.displacy as displacy

        options = {
            "ents": ["GOD", "PERSON", "PEOPLE GROUPS", "GPE", "tøp"],
            "colors": {"GOD": "purple", "PERSON": "#4facfe", "PEOPLE GROUPS": "orange", "GPE": "#98FB98", "tøp": "red"}
        }
        html = displacy.render(doc, style="ent", options=options)
        st.markdown(
            f"<div style='color: white; background: #2d2d2d; padding: 20px; border-radius: 10px; line-height: 2;'>{html}</div>",
            unsafe_allow_html=True)

        if st.button("← Back to Mission Command"):
            st.session_state.run_analysis = False
            st.rerun()
