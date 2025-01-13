import streamlit as st


def show_filter_menu():
    year = st.sidebar.selectbox('Year', options=[2024, 2025])
    return year
