import os
import streamlit as st
from conf_page import set_config_page


class Softskills_class:

    def get_softskills(self):
        set_config_page()
        st.subheader('Softskills')
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        img = os.path.join(BASE_DIR, '..', 'images', "comming_soon.png")
        st.image(img)