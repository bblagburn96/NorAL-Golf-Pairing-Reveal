import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# --- FORMAL CLUBHOUSE THEME ---
st.set_page_config(page_title="2026 NorAL Golf Invitational", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@400;700&display=swap');
    .stApp { background-color: #111827; color: #f3f4f6; }
    .header-box { text-align: center; padding: 40px 10px; border-bottom: 2px solid #374151; margin-bottom: 20px; background: linear-gradient(to bottom, #0f172a, #111827); }
    .main-title { font-family: 'Playfair Display', serif; font-size: 2.8em; color: #ffffff; font-style: italic; }
    .sub-title { font-family: 'Montserrat', sans-serif; font-size: 0.85em; text-transform: uppercase; letter-spacing: 4px; color: #9ca3af; }
    .reveal-card { background: #065f46; border: 2px solid #10b981; padding: 30px; margin-bottom: 30px; border-radius: 8px; text-align: center; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); } 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } }
    .team-card { background: #1f2937; border-left: 4px solid #059669; padding: 24px; margin-bottom: 16px; border-radius: 4px; text-align: center; }
    .team-label { font-family: 'Montserrat'; color: #9ca3af; font-size: 0.75em; font-weight: 700; text-transform: uppercase; margin-bottom: 12px; }
    .player-row { font-family: 'Montserrat'; font-size: 1.4em; letter-spacing: 1px; }
    .empty-slot { color: #374151; font-weight: 400; }
    .filled-slot { color: #ffffff; font-weight: 700; } 
    .stButton>button { background-color: #059669; color: white; font-weight: 700; border-radius: 4px; border: none; width: 100%; height: 3.8em; text-transform: uppercase; letter-spacing: 2px; }
    .stProgress > div > div > div > div { background-color: #059669; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # Changed worksheet name to NorALsheet
    return conn.read(worksheet="NorALsheet", ttl="5s")

# --- HEADER ---
st.markdown("<div class='header-box'><div class='main-title'>NorAL Golf Invitational</div><div class='sub-title'>2026 Team Selection</div></div>", unsafe_allow_html=True)

params = st.query_params
team_id = params.get("team_id")

df = load_data()

if team_id:
    # --- REGISTRATION VIEW ---
    st.markdown("<h2 style='text-align:center; font-family:Playfair Display;'>Official Tournament Entry</h2>", unsafe_allow_html=True)
    
    # Filter sheet for this team
    team_mask = df[df['team_id'] == int(team_id)]
    
    if len(team_mask) >= 2:
        st.warning(f"Team {team_id} is already full.")
        for name in team_mask['name'].tolist():
            st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{name}</div>", unsafe_allow_html=True)
        if st.button("Return to Field"):
            st.query_params.clear()
            st.rerun()
    else:
        name_entry = st.text_input("Full Name", placeholder="First & Last Name", label_visibility="collapsed")
        
        if st.button("Confirm Entry"):
            if not name_entry:
                st.error("Please enter a name.")
            elif name_entry.lower() in [n.lower() for n in df['name'].tolist()]:
                st.error("You are already registered!")
            else:
                # Add to DataFrame and Update Sheet
                new_row = pd.DataFrame([{"team_id": int(team_id), "name": name_entry.strip()}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="NorALsheet", data=updated_df)
                
                st.session_state['latest_name'] = name_entry
                st.session_state['latest_team'] = team_id
                st.session_state['latest_time'] = time.time()
                
                st.query_params.clear()
                st.rerun()
else:
    # --- DASHBOARD VIEW ---
    total_players = len(df)
    st.progress(min(total_players / 50, 1.0))
    
    if 'latest_time' in st.session_state and time.time() - st.session_state['latest_time'] < 15:
        st.markdown(f"<div class='reveal-card'><div style='font-size: 2em; font-weight: 700;'>{st.session_state['latest_name']}</div><div style='font-style: italic;'>Confirmed for Team {st.session_state['latest_team']}</div></div>", unsafe_allow_html=True)

    for i in range(1, 26):
        team_players = df[df['team_id'] == i]['name'].tolist()
        p1 = team_players[0] if len(team_players) > 0 else "---"
        p2 = team_players[1] if len(team_players) > 1 else "---"
        
        st.markdown(f"""
            <div class='team-card'>
                <div class='team-label'>Team {i}</div>
                <div class='player-row {"filled-slot" if p1 != "---" else "empty-slot"}'>{p1}</div>
                <div style='border-top: 1px solid #374151; width: 20%; margin: 8px auto;'></div>
                <div class='player-row {"filled-slot" if p2 != "---" else "empty-slot"}'>{p2}</div>
            </div>
        """, unsafe_allow_html=True)

    # ADMIN
    with st.expander("Tournament Director"):
        if st.text_input("Passcode", type="password") == "noral2026":
            if st.button("Reset Entire Field"):
                # Reset with correct headers
                reset_df = pd.DataFrame(columns=["team_id", "name", "category"])
                conn.update(worksheet="NorALsheet", data=reset_df)
                st.rerun()

    time.sleep(5)
    st.rerun()
