import streamlit as st
import pandas as pd
import time

# --- FORMAL CLUBHOUSE THEME ---
st.set_page_config(page_title="2026 NorAL Golf Invitational", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@400;700&display=swap');
    
    .stApp { background-color: #111827; color: #f3f4f6; }
    
    .header-box {
        text-align: center;
        padding: 40px 10px;
        border-bottom: 2px solid #374151;
        margin-bottom: 20px;
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
    
    .team-card {
        background: #1f2937;
        border-left: 4px solid #059669; 
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

    .player-row { font-family: 'Montserrat', sans-serif; font-size: 1.4em; letter-spacing: 1px; }
    .empty-slot { color: #374151; font-weight: 400; }
    .filled-slot { color: #ffffff; font-weight: 700; } 
    
    .stButton>button { 
        background-color: #059669; color: white; font-weight: 700; 
        border-radius: 4px; border: none; width: 100%; height: 3.8em;
        text-transform: uppercase; letter-spacing: 2px;
    }
    
    .stProgress > div > div > div > div { background-color: #059669; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ---
@st.cache_resource
def get_tournament_data():
    return {str(i): [] for i in range(1, 26)}

live_data = get_tournament_data()

# --- HEADER ---
st.markdown("<div class='header-box'><div class='main-title'>NorAL Golf Invitational</div><div class='sub-title'>2026 Team Selection</div></div>", unsafe_allow_html=True)

# --- NAVIGATION ---
params = st.query_params
team_id = params.get("team_id")

if team_id:
    # --- REGISTRATION VIEW ---
    st.markdown("<h2 style='text-align:center; font-family:Playfair Display;'>Official Tournament Entry</h2>", unsafe_allow_html=True)
    
    current_team = live_data.get(str(team_id), [])
    
    # Check if team is already full
    if len(current_team) >= 2:
        st.warning(f"Team {team_id} is already full.")
        st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{current_team[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{current_team[1]}</div>", unsafe_allow_html=True)
        if st.button("Return to Field"):
            st.query_params.clear()
            st.rerun()
    else:
        st.markdown("<p style='text-align:center; color:#9ca3af;'>Identify yourself to join the field.</p>", unsafe_allow_html=True)
        name_entry = st.text_input("Full Name", placeholder="First & Last Name", key="reg_input", label_visibility="collapsed")
        
        if st.button("Confirm Entry"):
            # Check for duplicate names in the whole field
            all_names = [name.lower() for team in live_data.values() for name in team]
            
            if not name_entry:
                st.error("Please enter a name.")
            elif name_entry.lower() in all_names:
                st.error(f"'{name_entry}' is already registered in the field!")
            else:
                live_data[str(team_id)].append(name_entry.strip())
                
                # Reveal Animation
                placeholder = st.empty()
                with placeholder.container():
                    st.markdown(f"<h3 style='text-align:center;'>Assigning Team Position...</h3>", unsafe_allow_html=True)
                    pb = st.progress(0)
                    for p in range(100):
                        time.sleep(0.01)
                        pb.progress(p + 1)
                
                placeholder.empty()
                st.toast(f"Welcome to Team {team_id}, {name_entry}!", icon="⛳")
                st.markdown(f"<h2 style='text-align:center; color:#059669;'>Confirmed: Team {team_id}</h2>", unsafe_allow_html=True)
                
                time.sleep(2.5)
                st.query_params.clear()
                st.rerun()

else:
    # --- DASHBOARD VIEW ---
    total_players = sum(len(names) for names in live_data.values())
    st.markdown(f"<p style='text-align:center; color:#9ca3af; font-size:0.8em; letter-spacing:2px;'>FIELD STATUS: {total_players} / 50 REGISTERED</p>", unsafe_allow_html=True)
    st.progress(total_players / 50)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 25 Teams
    for i in range(1, 26):
        members = live_data[str(i)]
        p1 = members[0] if len(members) > 0 else "---"
        p2 = members[1] if len(members) > 1 else "---"
        
        st.markdown(f"""
            <div class='team-card' id='team-{i}'>
                <div class='team-label'>Team {i}</div>
                <div class='player-row {"filled-slot" if p1 != "---" else "empty-slot"}'>{p1}</div>
                <div style='border-top: 1px solid #374151; width: 20%; margin: 8px auto;'></div>
                <div class='player-row {"filled-slot" if p2 != "---" else "empty-slot"}'>{p2}</div>
            </div>
        """, unsafe_allow_html=True)

    # Admin Reset
    st.markdown("---")
    with st.expander("Tournament Director"):
        admin_pass = st.text_input("Passcode", type="password")
        if admin_pass == "noral2026":
            if st.button("Reset Field"):
                live_data.update({str(i): [] for i in range(1, 26)})
                st.rerun()

    time.sleep(5)
    st.rerun()
