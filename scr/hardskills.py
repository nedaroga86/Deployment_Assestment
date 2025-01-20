import os
import streamlit as st
from conf_page import set_config_page


class Hardskills_class:

    def get_hardskills(self):
        set_config_page()
        st.subheader('Hardskills')
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        img = os.path.join(BASE_DIR, '..', 'images', "comming_soon.png")
        st.image(img)