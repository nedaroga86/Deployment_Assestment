import os
from main import Main_Program
import streamlit as st
from streamlit_space import space

page_bg_img = """
<style>
/* Change the background image */
[data-testid="stAppViewContainer"] {
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Optionally, set a background color */
[data-testid="stAppViewContainer"] {
    background-color: #D9D9D9; /* Change to your preferred color */
}

/* Optional: change sidebar background */
[data-testid="stSidebar"] {
    background-color: #f8f9fa; /* Change to your preferred sidebar color */#f8f9fa
}
</style>
"""


def choose_mode():
    if 'profile' in st.session_state:
        prog = Main_Program()
        prog.get_start()
    else:
        st.markdown(page_bg_img, unsafe_allow_html=True)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        st.header('Select your role in this assesment')
        space(lines=5)
        opt, opt2, opt3,opt4,opt5 = st.columns([1,3,3,3,1])
        with opt2:
            st.subheader('Autoevaluador')
            db_path = os.path.join(BASE_DIR,'..', 'images', 'auto.png')
            st.image(db_path, width=200)
            button = st.button('Choose', key='Autoevaluador')
            if button:
                st.session_state.profile = 'auto'
                st.rerun()

        with opt3:
            st.subheader('Team evaluador')
            db_path = os.path.join(BASE_DIR,'..', 'images', 'team.png')
            st.image(db_path, width=200)
            button = st.button('Choose', key='Team')
            if button:
                st.session_state.profile = 'team'
                st.rerun()

        with opt4:
            st.subheader('Stakeholder')
            db_path = os.path.join(BASE_DIR,'..', 'images', 'stake.png')
            st.image(db_path, width=200)
            button = st.button('Choose', key='stakeholder')
            if button:
                st.session_state.profile = 'stakeholder'
                st.rerun()
