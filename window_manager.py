import streamlit as st

def init_window_state():
    if 'open_windows' not in st.session_state:
        st.session_state.open_windows = []
    if 'active_window' not in st.session_state:
        st.session_state.active_window = None

def open_app(app_name):

    for window in st.session_state.open_windows:
        if window['id'] == app_name:

            window['minimized'] = False
            st.session_state.active_window = app_name
            st.session_state.start_menu_open = False 
            return

    new_window = {
        'id': app_name,
        'title': app_name,
        'minimized': False
    }
    st.session_state.open_windows.append(new_window)
    st.session_state.active_window = app_name
    st.session_state.start_menu_open = False 

def close_app(app_name):

    st.session_state.open_windows = [
        w for w in st.session_state.open_windows if w['id'] != app_name
    ]

    if st.session_state.active_window == app_name:
        st.session_state.active_window = None

def minimize_app(app_name):
    for window in st.session_state.open_windows:
        if window['id'] == app_name:
            window['minimized'] = True

    if st.session_state.active_window == app_name:
        st.session_state.active_window = None