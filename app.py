import os
import streamlit as st
from streamlit_option_menu import option_menu

#import the pages
from views.about import render_about
from views.methodology import render_methodology
from views.main import render_main

#establish API key for OpenAI API access
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

from pathlib import Path
from utils.build_PTA_vectordb import build_PTA_vectordb
from utils.build_past_obj_vectordb import build_past_case_vectordb

# -----------------------------
# Check and Build Vector Databases
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent

PTA_DB_FILE = (PROJECT_ROOT / "vectordb" / "legislation" / "chroma.sqlite3")

if not PTA_DB_FILE.exists():
    print("PTA vector database not found.")
    build_PTA_vectordb()
    print("PTA vector database built successfully.")


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
        width: 300px !important;
    }
    </style>
""", unsafe_allow_html=True)

#create a sidebar with navigation options
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["ℹ️ About Us", "🧩 Methodology", "🤖 Objection Assistant"],
        icons=["", "", ""],
        orientation="vertical",
        styles={
        "icon": {
            "display": "none",
        },
        "nav-link": {
            "font-size": "16px",
            "font-weight": "800",  
            "text-align": "left",
            "padding": "10px",
            "margin": "6px 0px",
            "--hover-color": "#eee",
            "color": "#0D47A1"
        },
        "nav-link-selected": {
            "font-size": "17px",
            "font-weight": "bold",
            "padding": "10px",
            "background-color": "#83BED8",
            "color": "white",
        },
        },
    )

if selected == "🤖 Objection Assistant":
    render_main()

elif selected == "🧩 Methodology":
    render_methodology()

elif selected == "ℹ️ About Us":
    render_about()

