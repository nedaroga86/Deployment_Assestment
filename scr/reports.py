import os

import streamlit as st

from conf_page import set_config_page


class Reports:

    def get_reports(self):
        set_config_page()
        st.subheader('Reporting')
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        img = os.path.join(BASE_DIR, '..', 'images', "comming_soon.png")
        st.image(img)