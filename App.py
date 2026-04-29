import streamlit as st
import pandas as pd
import time

# --- FORMAL CLUBHOUSE THEME ---
st.set_page_config(page_title="NorAL Golf | Team Selection", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@400;700&display=swap');
    
    .stApp { background-color: #0c1e12; color: #f4f1ea; }
    
    .logo-container {
        text-align: center;
        padding-top: 20px;
    }

    .golf-header {
        font-family: 'Playfair Display', serif; color: #d4af37;
        text-align: center; letter-spacing: 1px;
        padding-bottom: 5px; margin-top: 10px;
    }
    
    .team-card {
        background: linear-gradient(145deg, #122b1a, #0c1e12);
        border: 1px solid #d4af37; padding: 15px; margin-bottom: 12px;
        border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        text-align: center;
    }
    
    .player-row { font-family: 'Montserrat', sans-serif; font-size: 1.2em; padding: 8px 0; }
    .empty-slot { color: #2d4a36; font-style: italic; font-size: 0.9em; }
    .filled-slot { color: #ffffff; font-weight: bold; } 
    
    .stTextInput>div>div>input { background-color: #f4f1ea; color: #0c1e12; border-radius: 0; font-size: 1.2em; }
    .stButton>button { 
        background-color: #d4af37; color: #0c1e12; font-weight: bold; 
        border-radius: 0; border: none; width: 100%; height: 3.5em; font-size: 1.1em;
    }
    .download-btn { text-align: center; margin-top: 50px; opacity: 0.4; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO & TITLE SECTION ---
st.markdown("<div class='logo-container'>", unsafe_allow_html=True)

# Updated to look for your specific file name
try:
    st.image("IMG_4021.jpeg", width=220) 
except:
    st.markdown("⚠️ *[Please upload IMG_4021.jpeg to your GitHub repository]*")

st.markdown("<h1 class='golf-header'>2026 NorAL Golf Invitational</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#d4af37; font-family:Montserrat;'>Team Selection</h3>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- SHARED DATA BRAIN ---
@st.cache_resource
def get_tournament_data():
    return {str(i): [] for i in range(1, 26)}

live_data = get_tournament_data()

# --- ROUTING ---
params = st.query_params
team_id = params.get("team_id")

# --- VIEW 1: PLAYER SIGN-IN (Mobile View) ---
if team_id:
    st.markdown(f"<h2 style='text-align:center;'>Team Card: {team_id}</h2>", unsafe_allow_html=True)
    
    current_team = live_data.get(str(team_id), [])
    
    if len(current_team) >= 2:
        st.success("Registration Complete.")
        st.markdown(f"<div class='player-row filled-slot'>{current_team[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='player-row filled-slot'>{current_team[1]}</div>", unsafe_allow_html=True)
        if st.button("View Live Field"):
            st.query_params.clear()
            st.rerun()
    else:
        st.write("Please sign in to claim your position on this team.")
        name_entry = st.text_input("Enter Full Name", placeholder="e.g. Stacey Isom", key="reg_input")
        
        if st.button("Confirm & Join"):
            if name_entry:
                live_data[str(team_id)].append(name_entry.strip())
                st.balloons()
                time.sleep(2)
                st.query_params.clear()
                st.rerun()

# --- VIEW 2: THE DASHBOARD (Live Updates) ---
else:
    st.markdown("<h3 style='text-align:center;'>Live Field Updates</h3>", unsafe_allow_html=True)
    
    for i in range(1, 26):
        members = live_data[str(i)]
        p1 = members[0] if len(members) > 0 else "Awaiting Player..."
        p2 = members[1] if len(members) > 1 else "Awaiting Player..."
        
        st.markdown(f"""
            <div class='team-card'>
                <div style='color:#d4af37; font-size: 0.8em; font-weight: bold;'>Team {i}</div>
                <div class='player-row {"filled-slot" if p1 != "Awaiting Player..." else "empty-slot"}'>{p1}</div>
                <div style='border-top: 1px solid rgba(212,175,55,0.1); width: 30%; margin: 2px auto;'></div>
                <div class='player-row {"filled-slot" if p2 != "Awaiting Player..." else "empty-slot"}'>{p2}</div>
            </div>
        """, unsafe_allow_html=True)

    # Manual refresh
    time.sleep(5)
    st.rerun()
