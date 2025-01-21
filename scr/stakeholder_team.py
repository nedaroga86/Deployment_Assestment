import streamlit as st
from streamlit_space import space
from buttons_design import new_button, eliminate_button
from profile_team import save_stakeholder
from conf_page import set_config_page


def get_stakeholder_team(type_role, selected_employee):
    set_config_page()
    if 'mode_stake_holder' not in st.session_state:
        st.session_state.mode_stake_holder = False
    id_selected_employee = st.session_state.users_DB[st.session_state.users_DB['name']==selected_employee]['id'].iloc[0]
    define_stake_holder(id_selected_employee, type_role)


def define_stake_holder(id_selected_employee, type_role):
    id_stake_holder = st.session_state.users_DB[st.session_state.users_DB['id'] ==id_selected_employee]['stakeholder'].iloc[0]
    if id_stake_holder != '':
        stake_holder = st.session_state.users_DB[st.session_state.users_DB['id'] == id_stake_holder]['name'].iloc[0]
    else:
        stake_holder = 'To assign an Stakeholder'
    if not st.session_state.mode_stake_holder:
        sta, sta2,  = st.columns([2, 6])
        sta.selectbox('Stakeholder',options=[f'{stake_holder}'], index=0, disabled=True)

        if type_role == 'Team':
            if st.button('Update Stakeholder'):
                st.session_state.mode_stake_holder = True
                st.rerun()
    else:
        sta, sta2 = st.columns([2, 6])
        sta.markdown('#### Stakeholder')
        if stake_holder != '':
            options = [stake_holder] + list(st.session_state.users_DB['name'])
        else:
            options = st.session_state.users_DB['name']

        stake_holder = sta.selectbox('Stakeholder',
                                     options= options,
                                     index=0,
                                     label_visibility="collapsed")

        stake_holder = st.session_state.users_DB[st.session_state.users_DB['name'] == stake_holder]['id'].iloc[0]
        space()
        with sta:
            opt, opt2 = st.columns([2, 2])
            with opt2:
                if new_button('Confirm'):
                    save_stakeholder(stake_holder, id_selected_employee)
                    st.session_state.mode_stake_holder = False
                    st.rerun()
            with opt:
                if eliminate_button('Cancel'):
                    st.session_state.mode_stake_holder = False
                    st.rerun()
        space(lines=2)


