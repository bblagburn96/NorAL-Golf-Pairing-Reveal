import streamlit as st
import pandas as pd
import time

# --- FORMAL CLUBHOUSE THEME ---
st.set_page_config(page_title="2026 NorAL Golf Invitational", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@400;700&display=swap');
    
    /* Deep Clubhouse Charcoal & Forest Accents */
    .stApp { background-color: #111827; color: #f3f4f6; }
    
    .header-box {
        text-align: center;
        padding: 40px 10px;
        border-bottom: 2px solid #374151;
        margin-bottom: 30px;
        background: linear-gradient(to bottom, #0f172a, #111827);
    }

    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8em;
        color: #ffffff;
        margin-bottom: 5px;
        font-style: italic;
    }

    .sub-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 4px;
        color: #9ca3af;
    }
    
    /* Scorecard Card Styling */
    .team-card {
        background: #1f2937;
        border-left: 4px solid #059669; /* Masters Green Accent */
        padding: 24px;
        margin-bottom: 16px;
        border-radius: 4px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    
    .team-label {
        font-family: 'Montserrat', sans-serif;
        color: #9ca3af;
        font-size: 0.75em;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .player-row { 
        font-family: 'Montserrat', sans-serif; 
        font-size: 1.4em; 
        letter-spacing: 1px;
    }

    .empty-slot { color: #374151; font-weight: 400; }
    .filled-slot { color: #ffffff; font-weight: 700; } 
    
    /* Buttons: "The Green" Style */
    .stButton>button { 
        background-color: #059669; color: white; font-weight: 700; 
        border-radius: 4px; border: none; width: 100%; height: 3.8em;
        text-transform: uppercase; letter-spacing: 2px;
        font-family: 'Montserrat', sans-serif;
    }
    .stButton>button:hover { background-color: #10b981; color: white; }

    /* Clean Input */
    .stTextInput>div>div>input { background-color: #f9fafb; color: #111827; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class='header-box'>
        <div class='main-title'>NorAL Golf Invitational</div>
        <div class='sub-title'>2026 Team Selection</div>
    </div>
""", unsafe_allow_html=True)

# --- DATA ---
@st.cache_resource
def get_tournament_data():
    return {str(i): [] for i in range(1, 26)}

live_data = get_tournament_data()

# --- NAVIGATION ---
params = st.query_params
team_id = params.get("team_id")

if team_id:
    # --- PLAYER REGISTRATION ---
    st.markdown(f"<h2 style='text-align:center; font-family:Playfair Display;'>Pairing Card: {team_id}</h2>", unsafe_allow_html=True)
    
    current_team = live_data.get(str(team_id), [])
    
    if len(current_team) >= 2:
        st.success("Registration Finalized.")
        st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{current_team[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{current_team[1]}</div>", unsafe_allow_html=True)
        if st.button("Return to Leaderboard"):
            st.query_params.clear()
            st.rerun()
    else:
        st.markdown("<p style='text-align:center; color:#9ca3af;'>Claim your position on the 2026 roster.</p>", unsafe_allow_html=True)
        name_entry = st.text_input("Full Name", placeholder="Enter Name", key="reg_input", label_visibility="collapsed")
        
        if st.button("Confirm Entry"):
            if name_entry:
                live_data[str(team_id)].append(name_entry.strip())
                
                # --- COOL GOLF REVEAL ---
                placeholder = st.empty()
                with placeholder.container():
                    st.markdown("<h3 style='text-align:center;'>Registering...</h3>", unsafe_allow_html=True)
                    progress_bar = st.progress(0)
                    for percent_complete in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(percent_complete + 1)
                
                placeholder.empty()
                st.toast(f"Welcome to the Field, {name_entry}!", icon="🏌️")
                
                # A "Hole in One" subtle celebration
                st.markdown("<div style='text-align:center; font-size: 50px;'>⛳...🏌️...🏆</div>", unsafe_allow_html=True)
                
                time.sleep(1.5)
                st.query_params.clear()
                st.rerun()

else:
    # --- MAIN LEADERBOARD ---
    st.markdown("<p style='text-align:center; color:#6b7280; font-size:0.75em; letter-spacing:3px; margin-bottom:30px;'>LIVE TOURNAMENT FIELD</p>", unsafe_allow_html=True)
    
    for i in range(1, 26):
        members = live_data[str(i)]
        p1 = members[0] if len(members) > 0 else "---"
        p2 = members[1] if len(members) > 1 else "---"
        
        st.markdown(f"""
            <div class='team-card'>
                <div class='team-label'>Team {i}</div>
                <div class='player-row {"filled-slot" if p1 != "---" else "empty-slot"}'>{p1}</div>
                <div style='border-top: 1px solid #374151; width: 20%; margin: 8px auto;'></div>
                <div class='player-row {"filled-slot" if p2 != "---" else "empty-slot"}'>{p2}</div>
            </div>
        """, unsafe_allow_html=True)

    time.sleep(5)
    st.rerun()
