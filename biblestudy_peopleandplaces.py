import streamlit as st
import requests
import spacy
from spacy import displacy

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
        {"label": "GOD", "pattern": [{"LOWER": "his"}, {"LOWER": "son"}]},

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

text = "His brother's name was Jabal."

# Map specific phrases to their highlighted versions
# (Assuming blue = Person, green = Place)
replacements = {
    "brother's name was Jabal": "brother's name was \033[94mJabal\033[0m"
}

for original, highlighted in replacements.items():
    text = text.replace(original, highlighted)

print(text)

# --- 2. DATA LAYER: Fetch from Bible API ---
def get_bible_text(reference, trans="web"):
    try:
        # We add the translation as a 'query parameter' to the end of the URL
        url = f"https://bible-api.com/{reference}?translation={trans}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()['text']
        else:
            # This handles cases where the verse doesn't exist (e.g., "John 50:1")
            return None

    except Exception as e:
        # This handles internet connection issues
        st.error(f"Connection error: {e}")
        return None

# --- 3. UI LAYER: Streamlit Dashboard ---
st.set_page_config(page_title="AI Bible Study Partner", layout="wide")

st.title("🕊️ AI-Powered Bible Study")
st.write("Using Natural Language Processing to identify Divine, People, Places, and TØP references.")

# Sidebar Settings
st.sidebar.header("Settings")
ref = st.sidebar.text_input("Enter Reference:", "John 1:1-18")
show_stats = st.sidebar.checkbox("Show Entity Stats", value=True)

st.sidebar.header("Translation")
# We use a dictionary so the user sees "King James" but the code uses "kjv"
versions = {
    "World English Bible": "web",
    "King James Version": "kjv",
    "Bible in Basic English": "bbe"
}
selected_display_name = st.sidebar.selectbox("Version:", list(versions.keys()))
translation_code = versions[selected_display_name]

# Styling for the highlights
options = {
    "ents": ["GOD", "PERSON", "GPE", "TØP"],
    "colors": {
        "GOD": "purple",
        "PERSON": "#4facfe",  # vibrant blue
        "PEOPLE GROUP": "blue",
        "GPE": "#98FB98",  # Pale Green (Places)
        "TØP": "red"
    }
}

# BLACKLIST: Add words here that you want the AI to STOP highlighting
# (Case sensitive usually, so add variations if needed)
BLACKLIST = [
    "faith", "grace", "learn", "seek", "relieve", "amen", "life", "new moons",
    "sabbaths", "woe", "behold", "alas", "myrrh"
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