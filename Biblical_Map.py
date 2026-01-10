import streamlit as st
import spacy
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from itertools import combinations
import requests


# --- Load AI & API Logic (Reusing your previous functions) ---
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")


nlp = load_nlp()


def build_network_map(verses_list):
    # Create a NetworkX Graph
    G = nx.Graph()

    for verse in verses_list:
        doc = nlp(verse)
        # Identify entities (People and Places)
        entities = [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "GPE"]]

        # Remove duplicates in the same verse
        entities = list(set(entities))

        # Create a connection (edge) between every pair of people/places in this verse
        if len(entities) > 1:
            for pair in combinations(entities, 2):
                if G.has_edge(pair[0], pair[1]):
                    G[pair[0]][pair[1]]['weight'] += 1
                else:
                    G.add_edge(pair[0], pair[1], weight=1)

    # Convert to PyVis for a nice interactive web UI
    net = Network(height="500px", width="100%", bgcolor="#eeeeee", font_color="black")
    net.from_nx(G)

    # Save to a temporary file and return the HTML
    net.save_graph("bible_network.html")
    with open("bible_network.html", 'r', encoding='utf-8') as f:
        return f.read()


# --- Streamlit UI ---
st.title("🕸️ Biblical Cross-Reference Map")
st.write("Visualizing connections between People and Places.")

# Assuming you already have your 'raw_text' from the Bible API
# We split it into verses to find connections
if st.button("Generate Connection Map"):
    # (Using a sample text here - you can use your get_bible_text function)
    sample_verses = ["Jesus went to Galilee.", "Peter followed Jesus in Galilee.",
                     "John was also in Galilee with Peter."]

    graph_html = build_network_map(sample_verses)

    # Display the interactive graph in Streamlit
    components.html(graph_html, height=550)