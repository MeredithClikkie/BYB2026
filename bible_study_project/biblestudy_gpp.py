import streamlit as st
import pandas as pd
import plotly.express as px
import spacy
from spacy import displacy
import requests
import utils
from utils import is_blacklisted
from streamlit_timeline import timeline


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


# --- 4. SESSION STATE INITIALIZATION ---
if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

# --- 5. SIDEBAR SETTINGS & NAVIGATION ---
st.sidebar.header("Navigation")

# Home Button: Resets the app to the Welcome Page
if st.sidebar.button("🏠 Home / Reset"):
    st.session_state.run_analysis = False
    st.rerun()

st.sidebar.divider()

st.sidebar.header("Study Settings")
ref = st.sidebar.text_input("Enter Reference:", "Genesis 1:1")
show_stats = st.sidebar.checkbox("Show Stats", value=True)

versions = {"World English Bible": "web", "King James Version": "kjv"}
translation_code = versions[st.sidebar.selectbox("Version:", list(versions.keys()))]

# SINGLE Analyze button logic
if st.sidebar.button("🔍 Analyze Scripture"):
    st.session_state.run_analysis = True

options = {
    "ents": ["GOD", "PERSON", "PEOPLE GROUPS", "GPE", "tøp"],
    "colors": {
        "GOD": "purple",
        "PERSON": "#4facfe",
        "PEOPLE GROUPS": "orange",
        "GPE": "#98FB98",
        "tøp": "red"
    }
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


# CASE B: THE ANALYSIS PAGE
else:
    raw_text = get_bible_text(ref, trans=translation_code)

    if raw_text:
        book_name = ref.split()[0].title()

        # --- A. TIMELINE SECTION (The Protected Version) ---
        import importlib
        # 1. KEEP YOUR WORKING GENESIS LOGIC
        if book_name == "Genesis":
            st.subheader(f"⏳ Genesis: The Era of Beginnings")
            timeline_data = genesis.get_data(ref)  # This is your current working line
            timeline(timeline_data, height=600)

        # 2. KEEP YOUR WORKING EXODUS LOGIC
        elif book_name == "Exodus":
            st.subheader(f"⏳ Exodus: The Great Deliverance")
            timeline_data = exodus.get_data(ref)  # This is your current working line
            timeline(timeline_data, height=600)

        # 3. NEW GOSPEL WAVE LOGIC (The New "Switchboard")
        elif book_name in ["Matthew", "Mark", "Luke", "John"]:
            import importlib

            try:
                # This points all four books to your new gospels.py file
                book_module = importlib.import_module("gospels")
                st.subheader(f"⏳ The Life of Christ: Gospel Harmony")
                timeline_data = book_module.get_data(ref)
                if timeline_data and timeline_data.get("events"):
                    timeline(timeline_data, height=600)
            except ImportError:
                st.error("Gospels module not found. Check gospels.py location.")

        # NEW WAVE ROUTING
        elif book_name in ["Acts", "Romans", "Revelation"]:
            import importlib

            try:
                book_module = importlib.import_module("church")
                timeline_data = book_module.get_data(ref)

                # SAFETY CHECK: Only render if there are events
                if timeline_data and len(timeline_data.get("events", [])) > 0:
                    st.subheader("⛵ Apostolic Mission & The Early Church")
                    timeline(timeline_data, height=600)
                else:
                    # If no specific chapter data, show a placeholder message or nothing
                    st.info(f"Timeline intelligence for {ref} is currently being decrypted. Stay low.")

            except ImportError:
                st.error("Church module not found.")

        elif book_name in ["Psalms", "Proverbs", "Ecclesiastes", "Job"]:
            st.subheader("✍️ The Golden Age of Hebrew Poetry")
            book_module = importlib.import_module("wisdom")
            timeline_data = book_module.get_data(ref)
            timeline(timeline_data, height=600)

        elif book_name in ["Isaiah", "Jeremiah", "Ezekiel", "Daniel", "Malachi"]:
            st.subheader("📢 Prophetic Voice: The Exile & Restoration")
            book_module = importlib.import_module("prophets")
            timeline_data = book_module.get_data(ref)
            timeline(timeline_data, height=600)

        # 4. EVERYTHING ELSE (Fallback)
        else:
            events = get_fallback_timeline(ref)
            if events:
                st.subheader(f"⏳ Timeline: {book_name}")
                df = pd.DataFrame(events)
                fig = px.line(df, x="Date", y=[0] * len(df), markers=True, text="Event")
                fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

        # --- B. TEXT HIGHLIGHTING SECTION ---
        st.divider()
        st.subheader(f"📖 Scripture Analysis: {ref}")

        doc = nlp(raw_text)
        doc.ents = [e for e in doc.ents if not is_blacklisted(e.text) and e.label_ in options["ents"]]

        if show_stats:
            counts = doc.count_by(spacy.attrs.IDS['ENT_TYPE'])
            cols = st.columns(5)


            # Helper to get counts
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