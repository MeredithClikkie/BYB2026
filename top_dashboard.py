import streamlit as st
import pandas as pd
import plotly.express as px

st.title("|-/ The Clique Dashboard")

# Sidebar for filters
album = st.sidebar.selectbox("Select an Era", ["Vessel", "Blurryface", "Trench", "SAI", "Clancy"])

# Load your data

file_path = '/Users/meredithsmith/Desktop/TØPAnalysis/BreachSongs2.xlsx'
df = pd.read_excel(file_path)

st.header(f"Insights for the {album} Era")

# Example: Sentiment Chart
# fig = px.scatter(df[df['album'] == album], x='valence', y='sentiment', text='song_title')
# st.plotly_chart(fig)

st.write("Would you like me to help you write the code to perform sentiment analysis on your lyrics specifically?")