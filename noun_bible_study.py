import streamlit as st
import requests
import re

# --- 1. THE CATEGORIES: Define what words to highlight ---
# You can add as many words as you like to these lists
STUDY_FOCUS = {
    "People": {
        "words": ["Peter", "John", "James", "Mary", "Moses", "Paul", "David"],
        "color": "blue",
    },
    "Places": {
        "words": ["Jerusalem", "Galilee", "Bethlehem", "Jordan", "Egypt", "Zion", "Nazareth"],
        "color": "green",
    },
    "God/Spirit": {
        "words": ["Jesus", "Christ" "God", "Lord", "Spirit", "Father", "Almighty"],
        "color": "purple",
    }
}


# --- 2. THE HIGHLIGHTER: Word-level replacement logic ---
def highlight_specific_words(text):
    highlighted_text = text

    for category, data in STUDY_FOCUS.items():
        color = data['color']
        for word in data['words']:
            # \b ensures we match "God" but not "Godly"
            # re.IGNORECASE makes it match "jesus" and "Jesus"
            pattern = rf"\b({word})\b"

            # We wrap the matched word in an HTML span with a background color
            replacement = f'<span style="background-color: {color}; font-weight: bold; padding: 0 4px; border-radius: 3px;">\\1</span>'
            highlighted_text = re.sub(pattern, replacement, highlighted_text, flags=re.IGNORECASE)

    return highlighted_text


# --- 3. THE DATA: Fetch from Bible API ---
def get_bible_text(reference):
    try:
        url = f"https://bible-api.com/{reference}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['verses']
        else:
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None


# --- 4. THE UI: Streamlit Dashboard ---
st.set_page_config(page_title="Bible Word Study", layout="wide")

st.title("🔍 Word-Level Bible Study Tool")
st.write("This tool highlights specific **People**, **Places**, and **Titles** within the text.")

# Sidebar for Legend
st.sidebar.header("Color Legend")
for cat, data in STUDY_FOCUS.items():
    st.sidebar.markdown(
        f'<div style="background-color:{data["color"]}; padding:5px; border-radius:5px; margin-bottom:5px;">{cat}</div>',
        unsafe_allow_html=True)

# Input area
ref = st.text_input("Enter Reference (e.g., John 1, Matthew 2, Acts 1:1-10):", "John 4")

if st.button("Run Analysis"):
    data = get_bible_text(ref)

    if data:
        st.subheader(f"Scripture: {ref}")

        # We build one large block of text or display verse by verse
        for v in data:
            verse_num = v['verse']
            clean_text = v['text'].strip()

            # Run our highlighter
            formatted_verse = highlight_specific_words(clean_text)

            # Display in Streamlit
            st.markdown(f"**{verse_num}** {formatted_verse}", unsafe_allow_html=True)
    else:
        st.error("Reference not found. Please try again.")