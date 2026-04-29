import streamlit as st
import pandas as pd
import time

# --- MIDNIGHT STEEL THEME ---
st.set_page_config(page_title="2026 NorAL Golf Invitational", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;700&display=swap');
    
    /* Midnight Navy Background */
    .stApp { background-color: #020617; color: #f8fafc; }
    
    /* Centering and Title Styling */
    .logo-container { text-align: center; margin-bottom: 20px; }
    
    .golf-header {
        font-family: 'Playfair Display', serif; color: #f1f5f9;
        text-align: center; letter-spacing: 1px; margin-top: 10px;
    }
    
    /* Team Card Styling */
    .team-card {
        background: #0f172a;
        border: 1px solid #334155; 
        padding: 20px; margin-bottom: 15px;
        border-radius: 4px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        text-align: center;
    }
    
    .player-row { font-family: 'Inter', sans-serif; font-size: 1.25em; padding: 10px 0; }
    .empty-slot { color: #475569; font-style: italic; font-size: 0.95em; }
    .filled-slot { color: #f8fafc; font-weight: 700; } 
    
    /* Input & Button Styling */
    .stTextInput>div>div>input { background-color: #f8fafc; color: #020617; border-radius: 2px; font-size: 1.2em; }
    .stButton>button { 
        background-color: #f8fafc; color: #020617; font-weight: 700; 
        border-radius: 2px; border: none; width: 100%; height: 3.5em; font-size: 1.1em;
    }
    
    /* Force Centering for Streamlit Elements */
    [data-testid="stImage"] { display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("<div class='logo-container'>", unsafe_allow_html=True)

# Make sure you upload IMG_4021.jpeg to GitHub
try:
    st.image("IMG_4021.jpeg", width=240) 
except:
    st.info("Logo pending upload: IMG_4021.jpeg")

st.markdown("<h1 class='golf-header'>2026 NorAL Golf Invitational</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#94a3b8; font-family:Inter; font-weight:400; margin-top:-10px;'>Team Selection</h3>", unsafe_allow_html=True)
st.markdown("<div style='width:60px; height:2px; background:#94a3b8; margin: 20px auto;'></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- SHARED DATA ---
@st.cache_resource
def get_tournament_data():
    return {str(i): [] for i in range(1, 26)}

live_data = get_tournament_data()

# --- APP NAVIGATION ---
params = st.query_params
team_id = params.get("team_id")

# IF PLAYER SCANS A CARD
if team_id:
    st.markdown(f"<h2 style='text-align:center; font-family:Playfair Display;'>Team Card: {team_id}</h2>", unsafe_allow_html=True)
    
    current_team = live_data.get(str(team_id), [])
    
    if len(current_team) >= 2:
        st.success("Team 100% Locked.")
        st.markdown(f"<div class='player-row filled-slot'>{current_team[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='player-row filled-slot'>{current_team[1]}</div>", unsafe_allow_html=True)
        if st.button("Back to Selection Board"):
            st.query_params.clear()
            st.rerun()
    else:
        st.write("Enter your name as it appears on the roster to join this pairing.")
        name_entry = st.text_input("Full Name", placeholder="e.g. Stacey Isom", key="reg_input")
        
        if st.button("Confirm Selection"):
            if name_entry:
                live_data[str(team_id)].append(name_entry.strip())
                st.balloons()
                time.sleep(2)
                st.query_params.clear()
                st.rerun()

# MAIN DASHBOARD VIEW
else:
    st.markdown("<h4 style='text-align:center; color:#475569; letter-spacing:2px; text-transform:uppercase; margin-bottom: 20px;'>Live Pairings Dashboard</h4>", unsafe_allow_html=True)
    
    # Simple list of Team Cards
    for i in range(1, 26):
        members = live_data[str(i)]
        p1 = members[0] if len(members) > 0 else "Awaiting Player..."
        p2 = members[1] if len(members) > 1 else "Awaiting Player..."
        
        st.markdown(f"""
            <div class='team-card'>
                <div style='color:#94a3b8; font-size: 0.8em; font-weight: bold; text-transform: uppercase;'>Team {i}</div>
                <div class='player-row {"filled-slot" if p1 != "Awaiting Player..." else "empty-slot"}'>{p1}</div>
                <div style='border-top: 1px solid rgba(148, 163, 184, 0.1); width: 40%; margin: 5px auto;'></div>
                <div class='player-row {"filled-slot" if p2 != "Awaiting Player..." else "empty-slot"}'>{p2}</div>
            </div>
        """, unsafe_allow_html=True)

    # Automatic refresh every 5 seconds
    time.sleep(5)
    st.rerun()
