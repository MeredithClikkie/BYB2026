import streamlit as st
import pandas as pd
import plotly.express as px
import spacy
from spacy import displacy
import requests
import utils
from utils import is_blacklisted
from streamlit_timeline import timeline
import genesis

# 1. PAGE SETUP (MUST BE FIRST AND ONLY ONCE)
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


# --- 4. SIDEBAR SETTINGS ---
st.sidebar.header("Settings")
ref = st.sidebar.text_input("Enter Reference:", "Genesis 1:1")
show_stats = st.sidebar.checkbox("Show Stats", value=True)

versions = {"World English Bible": "web", "King James Version": "kjv"}
translation_code = versions[st.sidebar.selectbox("Version:", list(versions.keys()))]

options = {
    "ents": ["GOD", "PERSON", "PEOPLE GROUPS", "GPE", "tøp"],
    "colors": {"GOD": "purple", "PERSON": "#4facfe", "PEOPLE GROUPS": "orange", "GPE": "#98FB98", "tøp": "red"}
}

# --- 5. SESSION STATE LOGIC ---
if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

# Sidebar Button
if st.sidebar.button("Analyze Scripture"):
    st.session_state.run_analysis = True

# --- 6. PAGE RENDERING ---

# IF ANALYSIS IS NOT ACTIVE -> SHOW WELCOME PAGE
if not st.session_state.run_analysis:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
          ### Welcome to your AI Study Partner 📖
        This tool uses **Natural Language Processing** to help you dive deeper into the Bible.

        **To get started:**
        1. Enter a verse reference in the sidebar.
        2. Choose your preferred translation.
        3. Click **'Analyze Scripture'**!
            <style>
            :root { --bandito-yellow: #FCE300; --deep-grey: #212121; }
            .stApp { background-color: var(--deep-grey); color: white; }
            h1, h2, h3 { color: var(--bandito-yellow) !important; font-family: 'Courier New', Courier, monospace; }
            .stButton>button { background-color: var(--bandito-yellow); color: black; font-weight: bold; }
            </style>
        """, unsafe_allow_html=True)
        st.info("💡 **Tip:** Try looking up 'Genesis 7' to see the historical timeline in action.")

    with col2:
        try:
            st.image("welcome_torch.jpg", use_container_width=True)
        except:
            st.image("https://images.unsplash.com/photo-1504052434569-70ad5836ab65?q=80&w=1000")
        st.markdown("<div style='text-align: center; color: #FCE300;'>‖—‖ Keep your torch lit. ‖—‖</div>",
                    unsafe_allow_html=True)

# CASE B: THE ANALYSIS PAGE (Shows after clicking button)
else:
    # 1. FETCH TEXT (Works for any book: John, Romans, Psalm, etc.)
    raw_text = get_bible_text(ref, trans=translation_code)

    if raw_text:
        book_name = ref.split()[0].title()

        # --- A. TIMELINE SECTION ---
        # Special Interactive Box for Genesis
        if book_name == "Genesis":
            st.subheader(f"⏳ Historical Timeline: {book_name}")
            timeline_data = genesis.get_data()
            timeline(timeline_data, height=600)

        # Plotly Timeline for other books (like John)
        else:
            events = get_fallback_timeline(ref)
            if events:
                st.subheader(f"⏳ Timeline: {book_name}")
                df = pd.DataFrame(events)
                fig = px.line(df, x="Date", y=[0] * len(df), markers=True, text="Event")
                fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

        # --- B. TEXT HIGHLIGHTING SECTION (The "AI" part) ---
        st.divider()  # Visual break between timeline and text
        st.subheader(f"📖 Scripture Analysis: {ref}")

        doc = nlp(raw_text)
        # Filter Entities based on your options
        doc.ents = [e for e in doc.ents if not is_blacklisted(e.text) and e.label_ in options["ents"]]

        # Display Stats (Divine, People, Places)
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

        # Render the highlighted Bible text
        html = displacy.render(doc, style="ent", options=options)
        st.markdown(f"<div class='bible-container'>{html}</div>", unsafe_allow_html=True)

        # --- C. NAVIGATION ---
        if st.button("← Back to Welcome Page"):
            st.session_state.run_analysis = False
            st.rerun()

    else:
        st.error(f"Sorry, I couldn't find the text for '{ref}'. Check your spelling!")
        if st.button("Try a different verse"):
            st.session_state.run_analysis = False
            st.rerun()