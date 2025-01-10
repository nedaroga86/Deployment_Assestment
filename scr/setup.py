import streamlit as st

from conf_page import set_config_page


def manage_setup():

    if 'mode' not in st.session_state:
        st.session_state.mode = False

    set_config_page()