import streamlit as st
import pandas as pd
import numpy as np

# 1. Add a title and text
st.title("My First Streamlit App")
st.write("This app generates random data based on your input.")

# 2. Add interactive widgets
name = st.text_input("Enter your name", "Data Scientist")
data_points = st.slider("Number of data points", 10, 100, 50)

# 3. Logic and Visualization
if st.button("Generate Chart"):
    st.write(f"Hello {name}, here is your data:")
    chart_data = pd.DataFrame(
        np.random.randn(data_points, 2),
        columns=['Metric A', 'Metric B']
    )
    st.line_chart(chart_data)