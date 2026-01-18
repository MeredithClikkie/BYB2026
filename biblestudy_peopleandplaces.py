import streamlit as st
import pandas as pd
import plotly.express as px
import spacy
from spacy import displacy
import requests
import os
import sys
import utils
from utils import is_blacklisted

# 1. PAGE SETUP
st.set_page_config(page_title="Bible Study Partner", layout="wide")


# --- 1. AI SETUP ---
@st.cache_resource
def load_nlp():
    nlp = spacy.load("en_core_web_sm")

    # We add the ruler BEFORE the NER (Named Entity Recognizer)
    # Use 'overwrite_ents': True to make YOUR patterns the priority
    if "entity_ruler" not in nlp.pipe_names:
        config = {"overwrite_ents": True}
        ruler = nlp.add_pipe("entity_ruler", before="ner", config=config)

        # Base Patterns
        # PULL PATTERNS FROM UTILS.PY
        base_patterns = utils.get_base_patterns()
        ruler.add_patterns(base_patterns)
    return nlp

nlp = load_nlp()


# --- 2. DATA FUNCTIONS ---
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        return response.json()['text'] if response.status_code == 200 else None
    except Exception as e:
        return None


def get_fallback_timeline(reference):
    # This is used if a specific book file doesn't exist
    db = {
        "John": [
            {"Event": "Birth of Jesus", "Date": -4},
            {"Event": "Crucifixion", "Date": 30}
        ]
    }
    book = reference.split()[0].title()
    return db.get(book, [])


# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Bible Study Partner", layout="wide")
st.sidebar.header("Settings")
ref = st.sidebar.text_input("Enter Reference:", "Genesis 1:1")
show_stats = st.sidebar.checkbox("Show Stats", value=True)

versions = {"World English Bible": "web", "King James Version": "kjv"}
translation_code = versions[st.sidebar.selectbox("Version:", list(versions.keys()))]

options = {
    "ents": ["GOD", "PERSON", "PEOPLE GROUPS", "GPE", "tøp"],
    "colors": {"GOD": "purple", "PERSON": "#4facfe", "PEOPLE GROUPS": "orange", "GPE": "#98FB98", "tøp": "red"}
}
BLACKLIST = ["faith", "grace", "amen"]

# --- WELCOME PAGE (Shows only if button NOT clicked) ---

if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

if not st.session_state.run_analysis:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
          ### Welcome to your AI Study Partner 📖
        This tool uses **Natural Language Processing** to help you dive deeper into the Bible.

        **To get started:**
        1. Enter a verse reference in the sidebar (e.g., *Genesis 1* or *John 3*).
        2. Choose your preferred translation.
        3. Click **'Analyze Scripture'** to see the magic happen!
            <style>
            /* TØP Color Palette */
            :root {
                --bandito-yellow: #FCE300;
                --deep-grey: #212121;
            }
            .stApp {
                background-color: var(--deep-grey);
                color: white;
            }
            h1, h2, h3 {
                color: var(--bandito-yellow) !important;
                font-family: 'Courier New', Courier, monospace;
            }
            .stButton>button {
                background-color: var(--bandito-yellow);
                color: black;
                border-radius: 0px;
                font-weight: bold;
                border: none;
            }
            /* Style for the Bible text box */
            .bible-container {
                border-left: 5px solid var(--bandito-yellow);
                padding-left: 20px;
                background-color: #2b2b2b;
                border-radius: 5px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.info("💡 **Tip:** Try looking up 'Genesis 1' to see the historical timeline in action.")

    with col2:
        # Load the locally saved image
        try:
            st.image("welcome_torch.jpg", use_container_width=True)
            st.markdown("""
                <div style='text-align: center; color: #FCE300; font-family: monospace;'>
                    ‖—‖ Keep your torch lit. ‖—‖
                </div>
            """, unsafe_allow_html=True)
        except:
            # Fallback if the image file isn't found yet
            st.warning("Torch image not found. Ensure 'welcome_torch.jpg' is in your project folder.")
            st.image("https://images.unsplash.com/photo-1504052434569-70ad5836ab65?q=80&w=1000", caption="‖—‖")

# --- 4. MAIN EXECUTION ---
if st.sidebar.button("Analyze Scripture"):
    st.session_state.run_analysis = True # Record that we've started
    raw_text = get_bible_text(ref, trans=translation_code)

    if raw_text:
        doc = nlp(raw_text)
        book_name = ref.split()[0].title()

        # Filtering
        doc.ents = [
            e for e in doc.ents
            if not is_blacklisted(e.text) and e.label_ in options["ents"]]

        # --- TIMELINE ROUTER ---
        if book_name == "Genesis":
            events = genesis.get_data()
        else:
            events = get_fallback_timeline(ref)

        if events:
            st.subheader(f"⏳ Historical Timeline: {book_name}")
            df = pd.DataFrame(events)

            # Better Looking Plotly Timeline
            fig = px.line(df, x="Date", y=[0] * len(df), markers=True, text="Event")
            for i in range(len(df)):
                fig.add_shape(type='line', x0=df['Date'].iloc[i], y0=-0.1, x1=df['Date'].iloc[i], y1=0,
                              line=dict(color="grey", width=1, dash="dot"))

            fig.update_traces(textposition='top center', marker=dict(size=12, color='#7030a0', symbol='diamond'))
            fig.update_yaxes(visible=False, range=[-0.5, 0.5])
            fig.update_xaxes(showgrid=True, title="Year (BC < 0 > AD)", zeroline=True, zerolinecolor='black')
            fig.update_layout(height=300, margin=dict(l=40, r=40, t=20, b=40), plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        # --- STATS & TEXT ---
        if show_stats:
            counts = doc.count_by(spacy.attrs.IDS['ENT_TYPE'])
            cols = st.columns(5)


            def gc(label):
                # Check if the label exists in the strings first
                if label in nlp.vocab.strings:
                    l_id = nlp.vocab.strings[label]
                    return counts.get(l_id, 0)
                else:
                    return 0


            cols[0].metric("Divine", gc("GOD"))
            cols[1].metric("People", gc("PERSON"))
            cols[2].metric("Groups", gc("PEOPLE GROUPS"))
            cols[3].metric("Places", gc("GPE"))
            cols[4].metric("tøp", gc("tøp"))

        st.subheader(f"Scripture Text: {ref}")
        html = displacy.render(doc, style="ent", options=options)
        st.markdown(html, unsafe_allow_html=True)