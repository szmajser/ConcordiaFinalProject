import streamlit as st
import pandas as pd
from predict_page import show_predict_page
from explore_page import show_explore_page

page = st.sidebar.selectbox("Explore or Predict", ("Explore", "Predict"))

if page == "Predict":
    show_predict_page()
else:
    show_explore_page()