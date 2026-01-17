import streamlit as st
import requests
import spacy
from spacy import displacy
import re
import plotly.express as px
import pandas as pd
from streamlit_timeline import timeline


# Widget,Use Case
# st.text_input,Enter verse references or names.
# st.selectbox,"Choose between Bible versions (KJV, WEB, etc.)."
# st.file_uploader,Upload a PDF of a sermon to analyze.
# st.download_button,Save your highlighted study as a text file.
# st.camera_input,Take a photo of a physical Bible page to OCR (convert to text).

# --- 1. THE AI BRAIN: Load spaCy with Custom Theological Rules ---
@st.cache_resource
def load_nlp():
    # Load the base English model
    nlp = spacy.load("en_core_web_sm")

    # Create the EntityRuler to define custom categories
    # overwrite_ents=True ensures our "GOD" label takes priority over generic labels
    config = {"overwrite_ents": True}
    ruler = nlp.add_pipe("entity_ruler", before="ner", config=config)

    patterns = [
    # Define patterns for the "GOD" category
        {"label": "GOD", "pattern": [{"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "god"}, {"LOWER": "the"}, {"LOWER": "father"}]},
        {"label": "GOD", "pattern": [{"LOWER": "lord"}]},
        {"label": "GOD", "pattern": [{"LOWER": "jesus"}]},
        {"label": "GOD", "pattern": [{"LOWER": "christ"}]},
        {"label": "GOD", "pattern": [{"LOWER": "spirit"}]},
        {"label": "GOD", "pattern": [{"LOWER": "father"}, {"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "father"}, {"LOWER": "son"}]},
        {"label": "GOD", "pattern": [{"LOWER": "holy"}, {"LOWER": "ghost"}]},
        {"label": "GOD", "pattern": [{"LOWER": "holy"}, {"LOWER": "spirit"}]},
        {"label": "GOD", "pattern": [{"LOWER": "savior"}]},
        {"label": "GOD", "pattern": [{"LOWER": "yahweh"}]},
        {"label": "GOD", "pattern": [{"LOWER": "yahweh"},{"LOWER": "of"}, {"LOWER": "armies"}]},
        {"label": "GOD", "pattern": [{"LOWER": "holy"}, {"LOWER": "one"}]},
        {"label": "GOD", "pattern": [{"LOWER": "son"}, {"LOWER": "of"}, {"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "son"}, {"LOWER": "of"}, {"LOWER": "the"}, {"LOWER": "father"}]},
        {"label": "GOD", "pattern": [{"LOWER": "son"}, {"LOWER": "of"}, {"LOWER": "man"}]},
        {"label": "GOD", "pattern": [{"LOWER": "son"}, {"LOWER": "of"}, {"LOWER": "the"}, {"LOWER": "father"}]},
        {"label": "GOD", "pattern": [{"LOWER": "Immanuel"}]},
        {"label": "GOD", "pattern": [{"LOWER": "wonderful"}, {"LOWER": "counselor"}]},
        {"label": "GOD", "pattern": [{"LOWER": "mighty"}, {"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "mighty"}, {"LOWER": "one"}]},
        {"label": "GOD", "pattern": [{"LOWER": "everlasting"}, {"LOWER": "father"}, {"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "prince"}, {"LOWER": "of"}, {"LOWER": "peace"}]},
        {"label": "GOD", "pattern": [{"LOWER": "king"}, {"LOWER": "of"}, {"LOWER": "the"}, {"LOWER":"jews"}]},
        {"label": "GOD", "pattern": [{"LOWER": "his"}, {"LOWER": "Son"}]},

    # Add patterns for the "PERSON" category
        {"label": "PERSON", "pattern": [{"LOWER": "jacob"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "ahaz"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "uzziah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "pekah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "remaliah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "tabeel"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "maher"}, {"LOWER": "shalal"}, {"LOWER": "hash"}, {"LOWER": "baz"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "uriah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "gallim"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "tamar"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "amminadab"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "hezron"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "nahshon"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "salmon"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "boaz"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "obed"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "rehoboam"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "abijah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "asa"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "jehoshaphat"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "joram"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "shealtiel"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "jechoniah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "azor"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "zadok"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "eliud"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "eleazer"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "eliakim"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "achim"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "herod"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "moses"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "adam"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "cain"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "irad"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "mehujael"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "adah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "zillah"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "jubal"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "lamech"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "jabal"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "tubal-cain"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "tubal"}, {"LOWER": "cain"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "kenan"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "mahalalel"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "jared"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "enoch"}]},
        {"label": "PERSON", "pattern": [{"LOWER": "ham"}]},


    # Add patterns for the "PEOPLE GROUPS" category
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "philistine"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "syrians"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "assyrian"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "assyrians"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "jews"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "the"}, {"LOWER": "jews"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "jew"}]},
        {"label": "PEOPLE GROUPS", "pattern": [{"LOWER": "nazarene"}]},

    # Add patterns for the "GPE" category
        {"label": "GPE", "pattern": [{"LOWER": "sodom"}]},
        {"label": "GPE", "pattern": [{"LOWER": "gomorrah"}]},
        {"label": "GPE", "pattern": [{"LOWER": "zion"}]},
        {"label": "GPE", "pattern": [{"LOWER": "ephraim"}]},
        {"label": "GPE", "pattern": [{"LOWER": "shiloah"}]},
        {"label": "GPE", "pattern": [{"LOWER": "zebulon"}]},
        {"label": "GPE", "pattern": [{"LOWER": "galilee"}]},
        {"label": "GPE", "pattern": [{"LOWER": "manasseh"}]},
        {"label": "GPE", "pattern": [{"LOWER": "arpad"}]},
        {"label": "GPE", "pattern": [{"LOWER": "calno"}]},
        {"label": "GPE", "pattern": [{"LOWER": "carchemish"}]},
        {"label": "GPE", "pattern": [{"LOWER": "hamath"}]},
        {"label": "GPE", "pattern": [{"LOWER": "aiath"}]},
        {"label": "GPE", "pattern": [{"LOWER": "migron"}]},
        {"label": "GPE", "pattern": [{"LOWER": "michmash"}]},
        {"label": "GPE", "pattern": [{"LOWER": "ramah"}]},
        {"label": "GPE", "pattern": [{"LOWER": "gibeah"}]},
        {"label": "GPE", "pattern": [{"LOWER": "gebim"}]},
        {"label": "GPE", "pattern": [{"LOWER": "the"}, {"LOWER": "egyptian"}, {"LOWER": "sea"}]},
        {"label": "GPE", "pattern": [{"LOWER": "babylon"}]},
        {"label": "GPE", "pattern": [{"LOWER": "judea"}]},
        {"label": "GPE", "pattern": [{"LOWER": "bethlehem"}]},
        {"label": "GPE", "pattern": [{"LOWER": "land"}, {"LOWER": "of"}, {"LOWER": "havilah"}]},
        {"label": "GPE", "pattern": [{"LOWER": "land"}, {"LOWER": "of"}, {"LOWER": "cush"}]},
        {"label": "GPE", "pattern": [{"LOWER": "gihon"}]},
        {"label": "GPE", "pattern": [{"LOWER": "hiddekel"}]},
        {"label": "GPE", "pattern": [{"LOWER": "pishon"}]},
        {"label": "GPE", "pattern": [{"LOWER": "euphrates"}]},
        {"label": "GPE", "pattern": [{"LOWER": "tigris"}]},

        # Define patterns for the "TØP" category
        {"label": "TØP", "pattern": [{"LOWER": "necromancer"}]},
        {"label": "TØP", "pattern": [{"LOWER": "dead"}, {"LOWER": "on"}, {"LOWER": "behalf"}, {"LOWER": "of"}, {"LOWER": "the"}, {"LOWER": "living"}]}]


    ruler.add_patterns(patterns)
    return nlp

nlp = load_nlp()


# --- 2. DATA LAYER: Fetch from Bible API ---
def get_bible_text(reference, trans="web"):
    try:
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['text']
        else:
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None


def get_timeline_data(reference):
    timeline_db = {
        "Genesis": [
            {"Event": "Creation/Fall", "Date": -4000},
            {"Event": "The Flood", "Date": -2400},
            {"Event": "Call of Abraham", "Date": -2091},
            {"Event": "Joseph in Egypt", "Date": -1898}
        ],
        "Exodus": [
            {"Event": "Birth of Moses", "Date": -1526},
            {"Event": "The Exodus", "Date": -1446},
            {"Event": "Ten Commandments", "Date": -1445}
        ],
        "John": [
            {"Event": "Birth of Jesus", "Date": -4},
            {"Event": "Baptism of Jesus", "Date": 26},
            {"Event": "Crucifixion/Resurrection", "Date": 30}
        ]
    }
    book_name = reference.split()[0]
    return timeline_db.get(book_name, [])


# --- 3. UI LAYER: Streamlit Dashboard ---
# Move page config to the VERY TOP of the UI layer
st.set_page_config(page_title="AI Bible Study Partner", layout="wide")

st.title("🕊️ AI-Powered Bible Study")
st.write("Using NLP to identify Divine, People, Places, and TØP references.")

# Sidebar Settings
st.sidebar.header("Settings")
ref = st.sidebar.text_input("Enter Reference:", "John 1:1-18")
show_stats = st.sidebar.checkbox("Show Entity Stats", value=True)

st.sidebar.header("Translation")
versions = {"World English Bible": "web", "King James Version": "kjv", "Bible in Basic English": "bbe"}
selected_display_name = st.sidebar.selectbox("Version:", list(versions.keys()))
translation_code = versions[selected_display_name]

options = {
    "ents": ["GOD", "PERSON", "GPE", "TØP"],
    "colors": {"GOD": "purple", "PERSON": "#4facfe", "GPE": "#98FB98", "TØP": "red"}
}

BLACKLIST = ["faith", "grace", "learn", "seek", "relieve", "amen", "life", "new moons", "sabbaths", "woe", "behold",
             "alas", "myrrh"]

# --- MAIN LOGIC BLOCK ---
if st.sidebar.button("Analyze Scripture"):
    raw_text = get_bible_text(ref, trans=translation_code)

    if raw_text:
        doc = nlp(raw_text)

        # Filtering logic
        filtered_ents = []
        for ent in doc.ents:
            clean_entity_text = ent.text.strip().lower()
            if clean_entity_text not in BLACKLIST and ent.label_ in options["ents"]:
                filtered_ents.append(ent)
        doc.ents = filtered_ents

        # --- NEW & IMPROVED TIMELINE VISUALIZATION ---
        events = get_timeline_data(ref)
        if events:
            st.subheader(f"⏳ Historical Timeline: {ref.split()[0]}")
            df = pd.DataFrame(events)

            # Create line with markers
            fig = px.line(df, x="Date", y=[0] * len(df), markers=True, text="Event")

            # Add vertical stems
            for i in range(len(df)):
                fig.add_shape(type='line', x0=df['Date'].iloc[i], y0=-0.1, x1=df['Date'].iloc[i], y1=0,
                              line=dict(color="grey", width=1, dash="dot"))

            fig.update_traces(textposition='top center', marker=dict(size=12, color='#7030a0', symbol='diamond'))
            fig.update_yaxes(visible=False, range=[-0.5, 0.5])
            fig.update_xaxes(showgrid=True, title="Year (BC < 0 > AD)", zeroline=True, zerolinecolor='black')
            fig.update_layout(height=300, margin=dict(l=40, r=40, t=20, b=40), plot_bgcolor='rgba(0,0,0,0)')

            st.plotly_chart(fig, use_container_width=True)
            st.divider()

        # --- Stats Section ---
        if show_stats:
            counts = doc.count_by(spacy.attrs.IDS['ENT_TYPE'])
            st.subheader("Summary Stats")
            col1, col2, col3 = st.columns(3)


            def get_count(label):
                # Check if the label exists in the vocabulary
                if label in nlp.vocab.strings:
                    label_id = nlp.vocab.strings[label]
                    return counts.get(label_id, 0)
                else:
                    return 0


            col1.metric("Divine", get_count("GOD"))
            col2.metric("People", get_count("PERSON"))
            col3.metric("Places", get_count("GPE"))
            st.divider()

        # --- Main Text Display ---
        st.subheader(f"Scripture Text: {ref}")
        html = displacy.render(doc, style="ent", options=options)
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.error("Could not fetch that reference. Please check the format.")

st.info("Note: 'GPE' stands for Geopolitical Entity (Places/Locations).")