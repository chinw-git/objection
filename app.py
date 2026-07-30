import streamlit as st
from streamlit_option_menu import option_menu

#import the pages
from views.about import render_about
from views.methodology import render_methodology
from views.main import render_main

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["About Us", "Methodology", "Objection Assistant"],
        icons=["info-circle", "gear", "chat-left-text"],
        orientation="vertical",
        styles={
        "nav-link": {
            "font-size": "13px",   
            "text-align": "left",
            "--hover-color": "#eee",
        },
        "icon": {
            "font-size": "13px",
        },
        "nav-link-selected": {
            "font-size": "14px",
            "background-color": "#83BED8",
        },
        },
    )

if selected == "Objection Assistant":
    render_main()

elif selected == "Methodology":
    render_methodology()

elif selected == "About Us":
    render_about()

