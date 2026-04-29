import streamlit as st
import pandas as pd
import time

# --- CHAMPIONSHIP LEADERBOARD THEME ---
st.set_page_config(page_title="2026 NorAL Golf Invitational", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    /* Deep Slate/Midnight Background */
    .stApp { background-color: #020617; color: #f8fafc; }
    
    /* Elegant Text Header */
    .header-box {
        text-align: center;
        padding: 40px 10px;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 30px;
    }

    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2em;
        color: #ffffff;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }

    .sub-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: #94a3b8;
        font-weight: 600;
    }
    
    /* Tournament Card Styling */
    .team-card {
        background: #0f172a;
        border: 1px solid #334155; 
        padding: 24px;
        margin-bottom: 16px;
        border-radius: 2px;
        text-align: center;
        transition: border 0.3s ease;
    }
    
    .team-label {
        font-family: 'Inter', sans-serif;
        color: #64748b;
        font-size: 0.75em;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .player-row { 
        font-family: 'Inter', sans-serif; 
        font-size: 1.3em; 
        padding: 8px 0; 
    }

    .empty-slot { color: #334155; font-style: italic; }
    .filled-slot { color: #f8fafc; font-weight: 600; } 
    
    /* Clean Inputs & Buttons */
    .stTextInput>div>div>input { background-color: #f8fafc; color: #020617; border-radius: 0; border: none; font-size: 1.1em; }
    .stButton>button { 
        background-color: #f8fafc; color: #020617; font-weight: 700; 
        border-radius: 0; border: none; width: 100%; height: 3.8em;
        text-transform: uppercase; letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class='header-box'>
        <div class='main-title'>2026 NorAL Golf Invitational</div>
        <div class='sub-title'>Team Selection</div>
    </div>
""", unsafe_allow_html=True)

# --- SHARED DATA ---
@st.cache_resource
def get_tournament_data():
    return {str(i): [] for i in range(1, 26)}

live_data = get_tournament_data()

# --- NAVIGATION ---
params = st.query_params
team_id = params.get("team_id")

if team_id:
    # --- PLAYER REGISTRATION VIEW ---
    st.markdown(f"<h2 style='text-align:center; font-family:Playfair Display;'>Entry Card: Team {team_id}</h2>", unsafe_allow_html=True)
    
    current_team = live_data.get(str(team_id), [])
    
    if len(current_team) >= 2:
        st.success("Pairing Confirmed.")
        st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{current_team[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{current_team[1]}</div>", unsafe_allow_html=True)
        if st.button("View Tournament Field"):
            st.query_params.clear()
            st.rerun()
    else:
        st.markdown("<p style='text-align:center; color:#94a3b8;'>Enter your name to claim your spot.</p>", unsafe_allow_html=True)
        name_entry = st.text_input("Full Name", placeholder="e.g. Stacey Isom", key="reg_input", label_visibility="collapsed")
        
        if st.button("Submit Registration"):
            if name_entry:
                live_data[str(team_id)].append(name_entry.strip())
                st.balloons()
                time.sleep(2)
                st.query_params.clear()
                st.rerun()

else:
    # --- MAIN LEADERBOARD VIEW ---
    st.markdown("<p style='text-align:center; color:#64748b; font-size:0.8em; margin-bottom:30px;'>LIVE UPDATES FROM THE CLUBHOUSE</p>", unsafe_allow_html=True)
    
    for i in range(1, 26):
        members = live_data[str(i)]
        p1 = members[0] if len(members) > 0 else "Pending..."
        p2 = members[1] if len(members) > 1 else "Pending..."
        
        st.markdown(f"""
            <div class='team-card'>
                <div class='team-label'>Team {i}</div>
                <div class='player-row {"filled-slot" if p1 != "Pending..." else "empty-slot"}'>{p1}</div>
                <div style='border-top: 1px solid #1e293b; width: 30%; margin: 4px auto;'></div>
                <div class='player-row {"filled-slot" if p2 != "Pending..." else "empty-slot"}'>{p2}</div>
            </div>
        """, unsafe_allow_html=True)

    time.sleep(5)
    st.rerun()
