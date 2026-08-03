import streamlit as st
from streamlit_option_menu import option_menu

#import the pages
from views.about import render_about
from views.methodology import render_methodology
from views.main import render_main

#initialising the vector database for past objections if it doesn't exist
from pathlib import Path
from utils.build_past_obj_vectordb import build_past_case_vectordb

PROJECT_ROOT = Path(__file__).resolve().parent

VECTOR_DB_FILE = (PROJECT_ROOT / "vectordb" / "past_cases" / "chroma.sqlite3")

if not VECTOR_DB_FILE.exists():
    print("Past objection vector database not found.")
    build_past_case_vectordb()
    print("Past objection vector database built successfully.")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
        page_title="Property Tax Objection Assistant",
        page_icon="🏡",
        layout="wide"
    )

st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        width: 350px !important;
    }

    section[data-testid="stSidebar"] > div {
        width: 350px !important;
    }
    </style>
""", unsafe_allow_html=True)

#create a sidebar with navigation options
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["ℹ️ About Us", "⚙️ Methodology", "🤖 Objection Assistant"],
        icons=["", "", ""],
        orientation="vertical",
        styles={
        "icon": {
            "display": "none",
        },
        "nav-link": {
            "font-size": "15px",   
            "text-align": "left",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {
            "font-size": "17px",
            "background-color": "#83BED8",
        },
        },
    )

if selected == "🤖 Objection Assistant":
    render_main()

elif selected == "⚙️ Methodology":
    render_methodology()

elif selected == "ℹ️ About Us":
    render_about()

