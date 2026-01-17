import streamlit as st
import pandas as pd
import plotly.express as px
import spacy
from spacy import displacy
import requests
import os
import sys

# Ensure the app can see the 'books' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Modular Import
try:
    import books.genesis as genesis
except ImportError:
    st.error("Could not find books/genesis.py. Please check folder structure.")


# --- 1. AI SETUP ---
@st.cache_resource
def load_nlp():
    nlp = spacy.load("en_core_web_sm")
    config = {"overwrite_ents": True}
    ruler = nlp.add_pipe("entity_ruler", before="ner", config=config)

    # Base Patterns
    patterns = [
        {"label": "GOD", "pattern": [{"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "lord"}]},
        {"label": "GOD", "pattern": [{"LOWER": "jesus"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "moses"}]},
        {"label": "GPE", "pattern": [{"LOWER": "jerusalem"}]}
    ]
    ruler.add_patterns(patterns)
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
    "ents": ["GOD", "PERSON", "GPE", "TØP"],
    "colors": {"GOD": "purple", "PERSON": "#4facfe", "GPE": "#98FB98", "TØP": "red"}
}
BLACKLIST = ["faith", "grace", "amen"]

# --- 4. MAIN EXECUTION ---
if st.sidebar.button("Analyze Scripture"):
    raw_text = get_bible_text(ref, trans=translation_code)

    if raw_text:
        doc = nlp(raw_text)
        book_name = ref.split()[0].title()

        # Filtering
        doc.ents = [e for e in doc.ents if e.text.lower() not in BLACKLIST and e.label_ in options["ents"]]

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
            cols = st.columns(3)


            def gc(label):
                # Check if the label exists in the strings first
                if label in nlp.vocab.strings:
                    l_id = nlp.vocab.strings[label]
                    return counts.get(l_id, 0)
                else:
                    return 0


            cols[0].metric("Divine", gc("GOD"))
            cols[1].metric("People", gc("PERSON"))
            cols[2].metric("Places", gc("GPE"))

        st.subheader(f"Scripture Text: {ref}")
        html = displacy.render(doc, style="ent", options=options)
        st.markdown(html, unsafe_allow_html=True)