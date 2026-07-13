import streamlit as st
import time

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="NorAL Golf Invitational", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@400;700&display=swap');
    
    /* Kiosk Mode Overrides */
    header {visibility: hidden;} 
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}
    .block-container { padding: 1rem !important; max-width: 98% !important; }
    
    /* App Colors & Typography */
    .stApp { background-color: #111827; color: #f3f4f6; }
    
    .header-box { 
        text-align: center; 
        padding: 10px; 
        border-bottom: 2px solid #374151; 
        margin-bottom: 15px; 
        background: linear-gradient(to bottom, #0f172a, #111827); 
    }
    .main-title { 
        font-family: 'Playfair Display', serif; 
        font-size: 2.4em; 
        color: #ffffff; 
        font-style: italic; 
        margin-bottom: 0px;
    }
    .sub-title { 
        font-family: 'Montserrat', sans-serif; 
        font-size: 0.75em; 
        text-transform: uppercase; 
        letter-spacing: 4px; 
        color: #9ca3af; 
    }
    
    /* Grid System */
    .grid-container { 
        display: grid; 
        grid-template-columns: repeat(5, 1fr); 
        grid-template-rows: repeat(4, 1fr); 
        gap: 15px; 
        height: calc(100vh - 180px); 
    }
    .team-card { 
        background: #1f2937; 
        border: 2px solid #374151; 
        border-radius: 6px; 
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        align-items: center; 
        padding: 5px; 
    }
    
    /* Highlight Animation */
    .team-card.highlight { 
        background: #065f46; 
        border-color: #10b981; 
        animation: pulse 2s infinite; 
    }
    @keyframes pulse { 
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); } 
        70% { box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); } 
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } 
    }
    
    /* Typography inside cards */
    .team-label { font-family: 'Montserrat', sans-serif; font-size: 0.8em; color: #9ca3af; text-
