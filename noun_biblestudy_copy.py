import streamlit as st
import requests
import spacy
from spacy import displacy


# --- 1. THE AI BRAIN: Load spaCy with Custom Theological Rules ---
@st.cache_resource
def load_nlp():
    # Load the base English model
    nlp = spacy.load("en_core_web_sm")

    # Create the EntityRuler to define custom categories
    # overwrite_ents=True ensures our "GOD" label takes priority over generic labels
    config = {"overwrite_ents": True}
    ruler = nlp.add_pipe("entity_ruler", before="ner", config=config)

    # Define patterns for the "GOD" category
    patterns = [
        {"label": "GOD", "pattern": [{"LOWER": "god"}]},
        {"label": "GOD", "pattern": [{"LOWER": "lord"}]},
        {"label": "GOD", "pattern": [{"LOWER": "jesus"}]},
        {"label": "GOD", "pattern": [{"LOWER": "christ"}]},
        {"label": "GOD", "pattern": [{"LOWER": "spirit"}]},
        {"label": "GOD", "pattern": [{"LOWER": "father"}]},
        {"label": "GOD", "pattern": [{"LOWER": "holy"}, {"LOWER": "ghost"}]},
        {"label": "GOD", "pattern": [{"LOWER": "holy"}, {"LOWER": "spirit"}]},
        {"label": "GOD", "pattern": [{"LOWER": "savior"}]},
        {"label": "GOD", "pattern": [{"LOWER": "yahweh"}]},
        {"label": "GOD", "pattern": [{"LOWER": "holy"}, {"LOWER": "one"}]},

    # Add patterns for the "GPE" category
        {"label": "GPE", "pattern": [{"LOWER": "sodom"}]},
        {"label": "GPE", "pattern": [{"LOWER": "gomorrah"}]}
    ]

    ruler.add_patterns(patterns)
    return nlp


nlp = load_nlp()


# --- 2. DATA LAYER: Fetch from Bible API ---
def get_bible_text(reference):
    try:
        url = f"https://bible-api.com/{reference}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['text']
        else:
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None


# --- 3. UI LAYER: Streamlit Dashboard ---
st.set_page_config(page_title="AI Bible Study Partner", layout="wide")

st.title("🕊️ AI-Powered Bible Study")
st.write("Using Natural Language Processing to identify People, Places, and Divine references.")

# Sidebar Settings
st.sidebar.header("Settings")
ref = st.sidebar.text_input("Enter Reference:", "John 1:1-18")
show_stats = st.sidebar.checkbox("Show Entity Stats", value=True)

# Styling for the highlights
options = {
    "ents": ["GOD", "PERSON", "GPE"],
    "colors": {
        "GOD": "purple", # gradient purple
        "PERSON": "#4facfe",  # vibrant blue
        "GPE": "#98FB98"  # Pale Green (Places)
    }
}

# BLACKLIST: Add words here that you want the AI to STOP highlighting
# (Case sensitive usually, so add variations if needed)
BLACKLIST = [
    "faith", "grace", "learn", "seek", "relieve" "amen", "life", "new moons", "sabbaths"
]

if st.sidebar.button("Analyze Scripture"):
    raw_text = get_bible_text(ref)

    if raw_text:
        # Process the text through the AI pipeline
        doc = nlp(raw_text)

        # --- FILTERING LOGIC ---
        # We create a new list of entities that excludes the blacklist
        filtered_ents = []
        for ent in doc.ents:
            # Clean the text and make it lowercase for comparison
            clean_entity_text = ent.text.strip().lower()

            # If the word is NOT in our blacklist AND it's a category we care about
            if clean_entity_text not in BLACKLIST and ent.label_ in options["ents"]:
                filtered_ents.append(ent)

        # Tell the AI document to use our filtered list instead of its original list
        doc.ents = filtered_ents

        # --- Stats Section ---
        if show_stats:
            counts = doc.count_by(spacy.attrs.IDS['ENT_TYPE'])
            st.subheader("Summary Stats")
            col1, col2, col3 = st.columns(3)


            # Helper to get count for a label
            def get_count(label):
                label_id = nlp.vocab.strings[label]
                return counts.get(label_id, 0)


            col1.metric("Divine References", get_count("GOD"))
            col2.metric("People Found", get_count("PERSON"))
            col3.metric("Places Found", get_count("GPE"))
            st.divider()

        # --- Main Text Display ---
        st.subheader(f"Scripture Text: {ref}")

        # Generate the HTML using displacy
        html = displacy.render(doc, style="ent", options=options)

        # Streamlit needs 'unsafe_allow_html' to render the colored spans
        st.markdown(html, unsafe_allow_html=True)

    else:
        st.error("Could not fetch that reference. Please check the format (e.g., 'John 3:16' or 'Genesis 1').")

# --- Footer Info ---
st.info("Note: 'GPE' stands for Geopolitical Entity (Places/Locations).")