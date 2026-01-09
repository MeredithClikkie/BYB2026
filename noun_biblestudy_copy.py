import streamlit as st
import requests
import spacy
from spacy import displacy


# Load the AI model
# we use @st.cache_resource so it only loads once (saves memory)
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")


nlp = load_nlp()


# --- API Fetcher ---
def get_bible_text(reference):
    url = f"https://bible-api.com/{reference}"
    response = requests.get(url)
    return response.json()['text'] if response.status_code == 200 else None


# --- UI Setup ---
st.set_page_config(page_title="AI Bible Study", layout="wide")
st.title("🤖 AI Named Entity Recognition (NER) Bible Study")
st.write("The AI will automatically find **People (PERSON)** and **Places (GPE)**.")

ref = st.text_input("Enter Reference (e.g., Genesis 1 or Acts 2):", "Genesis 1")

if st.button("Analyze with AI"):
    raw_text = get_bible_text(ref)

    if raw_text:
        # The AI "reads" the whole text here
        doc = nlp(raw_text)

        # We tell spaCy to only highlight God Persons and Locations (GPE)
        options = {"ents": ["GOD", "PERSON", "GPE"],
                   "colors": {"GOD": "purple", "PERSON": "blue", "GPE": "green"}}

        # Generate the professional HTML visualizer
        html = displacy.render(doc, style="ent", options=options)

        # Display in Streamlit
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.error("Text not found.")