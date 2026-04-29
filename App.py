import streamlit as st
import pandas as pd
import time

# --- CHAMPIONSHIP LEADERBOARD THEME ---
st.set_page_config(page_title="2026 NorAL Golf Invitational", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    /* Midnight Navy Background */
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
        font-size: 2.5em;
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
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .team-label {
        font-family: 'Inter', sans-serif;
        color: #64748b;
        font-size: 0.8em;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }

    .player-row { 
        font-family: 'Inter', sans-serif; 
        font-size: 1.4em; 
        padding: 10px 0; 
    }

    .empty-slot { color: #1e293b; font-style: italic; font-weight: 400; }
    .filled-slot { color: #f8fafc; font-weight: 700; } 
    
    /* Clean Inputs & Buttons */
    .stTextInput>div>div>input { background-color: #f8fafc; color: #020617; border-radius: 0; border: none; font-size: 1.2em; }
    .stButton>button { 
        background-color: #f8fafc; color: #020617; font-weight: 800; 
        border-radius: 0; border: none; width: 100%; height: 4em;
        text-transform: uppercase; letter-spacing: 2px;
    }
    
    /* Hide Streamlit Branding for Professionalism */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
    <div class='header-box'>
        <div class='main-title'>2026 NorAL Golf Invitational</div>
        <div class='sub-title'>Team Selection</div>
    </div>
""", unsafe_allow_html=True)

# --- SHARED MEMORY (The Field) ---
@st.cache_resource
def get_tournament_data():
    return {str(i): [] for i in range(1, 26)}

live_data = get_tournament_data()

# --- APP ROUTING ---
params = st.query_params
team_id = params.get("team_id")

# --- VIEW 1: PLAYER REGISTRATION (Mobile Scanned Card) ---
if team_id:
    st.markdown(f"<h2 style='text-align:center; font-family:Playfair Display; margin-bottom:10px;'>Entry Card: Team {team_id}</h2>", unsafe_allow_html=True)
    
    current_team = live_data.get(str(team_id), [])
    
    if len(current_team) >= 2:
        st.success("Pairing Confirmed.")
        st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{current_team[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{current_team[1]}</div>", unsafe_allow_html=True)
        if st.button("View Live Field"):
            st.query_params.clear()
            st.rerun()
    else:
        st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom:20px;'>Enter your name to claim your spot on this team.</p>", unsafe_allow_html=True)
        name_entry = st.text_input("Full Name", placeholder="First & Last Name", key="reg_input", label_visibility="collapsed")
        
        if st.button("Confirm Selection"):
            if name_entry:
                live_data[str(team_id)].append(name_entry.strip())
                
                # SILVER CONFETTI & TOAST
                st.snow()
                st.toast(f"Slot Secured for Team {team_id}", icon="⛳")
                
                time.sleep(2.5)
                st.query_params.clear()
                st.rerun()
            else:
                st.warning("Identification is required.")

# --- VIEW 2: THE MAIN DASHBOARD (Leaderboard) ---
else:
    st.markdown("<p style='text-align:center; color:#475569; font-size:0.85em; letter-spacing:2px; margin-bottom:30px;'>LIVE CLUBHOUSE UPDATES</p>", unsafe_allow_html=True)
    
    # 25 Teams list
    for i in range(1, 26):
        members = live_data[str(i)]
        p1 = members[0] if len(members) > 0 else "Awaiting Player..."
        p2 = members[1] if len(members) > 1 else "Awaiting Player..."
        
        st.markdown(f"""
            <div class='team-card'>
                <div class='team-label'>Team {i}</div>
                <div class='player-row {"filled-slot" if p1 != "Awaiting Player..." else "empty-slot"}'>{p1}</div>
                <div style='border-top: 1px solid #1e293b; width: 40%; margin: 6px auto;'></div>
                <div class='player-row {"filled-slot" if p2 != "Awaiting Player..." else "empty-slot"}'>{p2}</div>
            </div>
        """, unsafe_allow_html=True)

    # 5-second auto-refresh
    time.sleep(5)
    st.rerun()
