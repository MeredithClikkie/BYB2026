# %% [markdown]
# # Isaiah
# %% [markdown]
# ### BYBW1 Relationship Between God and Humanity
# ### D6 Isaiah 1-6
# %% [markdown]
# https://biblehub.com/esv/isaiah/1.htm
# %%
import pandas as pd
import re
# %%
 # Thematic configuration
import streamlit as st
import requests

# --- 1. THE BRAIN: Your Thematic Dictionary ---
THEMES = {
    "Attributes of God": {
        "keywords": ["holy", "eternal", "almighty", "faithful", "love", "sovereign", "Lord", "God"],
        "color": "#FFC0CB"  # Pink
    },
    "Commands": {
        "keywords": ["thou shalt", "repent", "follow", "do not", "go", "pray", "believe"],
        "color": "#ADD8E6"  # Light Blue
    },
    "Promises": {
        "keywords": ["will give", "inheritance", "peace", "not be shaken", "with you", "comfort"],
        "color": "#90EE90"  # Light Green
    },
    "People": {
        "keywords": ["Isaiah", "God"],
        "color": "#FFC0CB"

    },
    "Places": {
        "keywords": ["Jerusalem"],
        "color": "#FFC0CB"
    }
}


# --- 2. THE ENGINE: Highlighting Logic ---
def highlight_verse(text):
    for theme, data in THEMES.items():
        if any(word.lower() in text.lower() for word in data['keywords']):
            return f'''<div style="background-color: {data["color"]}; padding: 12px; 
                       border-radius: 8px; margin: 8px 0; border-left: 5px solid #555;">
                       <small style="color: #555;">{theme.upper()}</small><br>{text}</div>'''

    return f'<div style="padding: 10px; border-bottom: 1px solid #eee;">{text}</div>'


# --- 3. THE DATA: API Fetcher ---
def get_bible_text(reference):
    try:
        url = f"https://bible-api.com/{reference}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['verses']  # Returns a list of verse objects
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None


# --- 4. THE UI: Streamlit Dashboard ---
st.set_page_config(page_title="Bible Study Coder", page_icon="📖")
st.title("📖 Thematic Bible Highlighter")

ref = st.text_input("Enter a Bible Reference (e.g., Psalm 23 or John 1:1-5):", "John 1:1-5")

if st.button("Analyze Scripture"):
    data = get_bible_text(ref)

    if data:
        st.subheader(f"Results for {ref}")
        for v in data:
            # v['text'] is the actual verse string from the API
            highlighted_html = highlight_verse(v['text'].strip())
            st.markdown(highlighted_html, unsafe_allow_html=True)
    else:
        st.error("Could not find that reference. Please check your spelling.")