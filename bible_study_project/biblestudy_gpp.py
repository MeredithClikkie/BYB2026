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

    # 1. DEFINE THE COLUMNS HERE
    col1, col2 = st.columns([2, 1])

    # 2. PUT YOUR TEXT IN COL1
    with col1:
        st.markdown("""
            ### Welcome to the Trench Study 📖
            This AI tool helps you navigate the layers of Scripture.

            **Mission Protocol:**
            1. Initialize reference in sidebar.
            2. Choose translation version.
            3. Deploy **'Analyze Scripture'**.
            """, unsafe_allow_html=True)

        st.info(f"💡 **Status:** Ready to analyze {book} {chapter}. Stay low.💡")

    # 3. PUT YOUR IMAGE IN COL2
    with col2:
        try:
            # This try block handles the "Bad filename" error by falling back to the URL
            st.image("welcome_torch.jpg", use_container_width=True)
        except:
            st.image("https://images.unsplash.com/photo-1504052434569-70ad5836ab65?q=80&w=1000")

        st.markdown("<div style='text-align: center; color: #FCE300;'>‖—‖ keep your torch lit ‖—‖</div>",
                    unsafe_allow_html=True)

    st.divider()
    # Normalize the book name for dictionary lookups
    clean_book = book.strip().title()

    # Organized Tabs
    t1, t2, t3, t4 = st.tabs(["📝 Trivia", "📚 Hangman", "📡 Resources", "📓 Journal"])

    with t1:  # TRIVIA
        questions = dm.get_trivia_questions(book, chapter)
        if not questions:
            questions = dm.get_auto_trivia(book, chapter)

        if questions and not st.session_state.game_over:
            q = questions[st.session_state.current_q]
            st.subheader(f"Question {st.session_state.current_q + 1}")
            st.write(f"### {q['question']}")

            with st.form("trivia_form"):
                choice = st.radio("Answer:", q['options'])
                submitted = st.form_submit_button("Submit Answer")

            if submitted:
                if choice == q['answer']:
                    st.success(f"Correct! {q.get('reference', '')}")
                    st.session_state.score += 1
                else:
                    st.error(f"Wrong! Answer: {q['answer']}")

                if st.session_state.current_q + 1 < len(questions):
                    st.session_state.current_q += 1
                else:
                    st.session_state.game_over = True

                st.button("Continue to Next Question")  # Triggers rerun on click

    with t2:  # HANGMAN
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

    with t3:  # RESOURCES
        st.header(f"Mission Assets: {book}")
        r_col1, r_col2 = st.columns(2)

        with r_col1:
            st.subheader("Quick Links")
            st.link_button("GotQuestions Overview", dm.get_gotquestions_url(book, chapter), use_container_width=True)
            bh_url = f"https://biblehub.com/{book.lower().replace(' ', '_')}/{chapter}.htm"
            st.link_button("Bible Hub Interlinear", bh_url, use_container_width=True)

            st.divider()
            st.subheader("🎧 Atmosphere")
            show_audio = st.toggle("Enable Lofi Study Music")
            if show_audio:
                st.video("https://www.youtube.com/watch?v=qXPoj_VYb3U")

        with r_col2:
            st.subheader("BibleProject Briefing")
            bp_url = dm.get_bible_project_url(book)
            if bp_url:
                st.video(bp_url)

    with t4:  # JOURNAL & PROGRESS
        st.header("📓 Tactical Journal & Mission Progress")

        prog_col, prompt_col = st.columns([1, 1])
        with prog_col:
            st.subheader("Progress Tracker")
            all_books = list(dm.BIBLE_CHAPTER_COUNTS.keys())
            read_books = st.multiselect("Completed Books:", options=all_books,
                                        default=st.session_state.get("completed_books", []), key="prog_track")
            st.session_state.completed_books = read_books
            st.progress(len(read_books) / 66)
            st.write(f"Objective: **{round((len(read_books) / 66) * 100, 1)}%** complete.")

        with prompt_col:
            st.subheader("Chapter Insight")
            # Uses the standardized LASB_PROMPTS for the book or a default
            insight = dm.LASB_PROMPTS.get('O', "Analyze the current context and recorded history.")
            st.info(f"**Focus for {book}:**\n\n{insight}")

        st.divider()
        st.subheader("📝 Life Application Study Notes (S.O.A.P.)")

        # Consistent Key Naming for the Text Areas
        s1, s2 = st.columns(2)
        with s1:
            st.text_area("📖 Scripture (S)", placeholder=dm.LASB_PROMPTS.get('S'), key=f"soap_s_{book}_{chapter}")
            st.text_area("🛠️ Application (A)", placeholder=dm.LASB_PROMPTS.get('A'), key=f"soap_a_{book}_{chapter}")
        with s2:
            st.text_area("🧐 Observation (O)", placeholder=dm.LASB_PROMPTS.get('O'), key=f"soap_o_{book}_{chapter}")
            st.text_area("🙏 Prayer (P)", placeholder=dm.LASB_PROMPTS.get('P'), key=f"soap_p_{book}_{chapter}")

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
