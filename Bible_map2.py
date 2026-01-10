import streamlit as st
import spacy
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from itertools import combinations
import requests


# --- 1. SETUP: AI & Bible API ---
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")


nlp = load_nlp()


def get_bible_verses(reference):
    try:
        url = f"https://bible-api.com/{reference}"
        response = requests.get(url)
        if response.status_code == 200:
            # Returns a list of strings (each verse)
            return [v['text'] for v in response.json()['verses']]
        return None
    except:
        return None


# --- 2. LOGIC: Build the Network ---
def build_network_map(verses_list):
    G = nx.Graph()

    for verse in verses_list:
        doc = nlp(verse)
        # Identify entities and their labels
        # We store them as tuples (Name, Label)
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "GPE"]:
                entities.append((ent.text.strip(), ent.label_))

        # Remove duplicates within the same verse
        entities = list(set(entities))

        # Add Nodes with Colors
        for name, label in entities:
            color = "#FFD700" if label == "PERSON" else "#98FB98"
            G.add_node(name, color=color, title=label)  # 'title' shows on hover

        # Create Edges (Connections)
        if len(entities) > 1:
            # We only need the names for the combinations
            names = [e[0] for e in entities]
            for pair in combinations(names, 2):
                if G.has_edge(pair[0], pair[1]):
                    G[pair[0]][pair[1]]['weight'] += 1
                else:
                    G.add_edge(pair[0], pair[1], weight=1, color="#888888")

    # --- 3. RENDERING: PyVis ---
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    net.from_nx(G)

    # Optional: Make the physics "bouncy" and interactive
    net.toggle_physics(True)

    # Save and return HTML
    path = "bible_network.html"
    net.save_graph(path)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


# --- 4. UI: Streamlit Dashboard ---
st.set_page_config(page_title="Bible Network Mapper", layout="wide")
st.title("🕸️ Biblical Connection Mapper")
st.write("Visualizing how People and Places interact across Scripture.")

ref = st.text_input("Enter Reference (e.g., Acts 1 or John 1:1-20):", "John 4")

if st.button("Generate Map"):
    with st.spinner("Analyzing connections..."):
        verses = get_bible_verses(ref)

        if verses:
            graph_html = build_network_map(verses)

            # Display Legend
            st.markdown("""
            **Legend:** <span style="color:#FFD700; font-weight:bold;">● People</span> | 
            <span style="color:#2E8B57; font-weight:bold;">● Places</span>
            """, unsafe_allow_html=True)

            # Show the Interactive Graph
            components.html(graph_html, height=650)
        else:
            st.error("Could not find that reference. Check your internet or spelling.")