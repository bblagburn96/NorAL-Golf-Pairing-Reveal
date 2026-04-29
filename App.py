import streamlit as st
import pandas as pd
import time

# --- FORMAL "MIDNIGHT STEEL" THEME ---
st.set_page_config(page_title="NorAL Golf | Team Selection", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;700&display=swap');
    
    /* Background: Deep Midnight Navy */
    .stApp { background-color: #020617; color: #f8fafc; }
    
    /* Title Styling */
    .golf-header {
        font-family: 'Playfair Display', serif; color: #f1f5f9;
        text-align: center; letter-spacing: 1px;
        margin-top: 10px;
    }
    
    /* Card Styling: Slate Navy with Silver Border */
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
    
    /* Input Styling */
    .stTextInput>div>div>input { background-color: #f8fafc; color: #020617; border-radius: 2px; font-size: 1.2em; border: none; }
    
    /* Button Styling: Silver/Slate Blue */
    .stButton>button { 
        background-color: #f8fafc; color: #020617; font-weight: 700; 
        border-radius: 2px; border: none; width: 100%; height: 3.5em; font-size: 1.1em;
        transition: 0.2s;
    }
    .stButton>button:hover { background-color: #cbd5e1; }

    /* Centering the Image container */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO & TITLE (Centered) ---
cols = st.columns([1, 2, 1])
with cols[1]:
    try:
        st.image("IMG_4021.jpeg", width=240) 
    except:
        st.info("Logo pending upload: IMG_4021.jpeg")

st.markdown("<h1 class='golf-header'>2026 NorAL Golf Invitational</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#94a3b8; font-family:Inter; font-weight:400; margin-top:-10px;'>Team Selection</h3>", unsafe_allow_html=True)
st.markdown("<div style='width:60px; height:2px; background:#94a3b8; margin: 20px auto;'></div>", unsafe_allow_html=True)

# --- SHARED DATA BRAIN ---
@st.cache_resource
def get_tournament_data():
    return {str(i): [] for i in range(1, 26)}

live_data = get_tournament_data()

# --- ROUTING ---
params = st.query_params
team_id = params.get("team_id")

# --- VIEW 1: PLAYER SIGN-IN ---
if team_id:
    st.markdown(f"<h2 style='text-align:center; font-family:Playfair Display;'>Team Card: {team_id}</h2>", unsafe_allow_html=True)
    
    current_team = live_data.get(str(team_id), [])
    
    if len(current_team) >= 2:
        st.success("Team 100% Locked.")
        st.markdown(f"<div class='player-row filled-slot'>{current_team[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='player-row filled-slot'>{current_team[1]}</div>", unsafe_allow_html=True)
        if st.button("Back to Field"):
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

# --- VIEW 2: THE DASHBOARD ---
else:
    st.markdown("<h4 style='text-align:center; color:#475569; letter-spacing:2px; text-transform:uppercase;'>Live Pairings Dashboard</h4>", unsafe_allow_html=True)
    
    # Grid of Cards
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

    # Auto-refresh
    time.sleep(5)
    st.rerun()

Your slide deck and app code are now perfectly synced! Take a look at the design and let me know if those Navy and Silver tones hit the mark for the event.
