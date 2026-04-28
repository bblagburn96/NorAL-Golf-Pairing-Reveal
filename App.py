import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# --- Style & Theme ---
st.set_page_config(page_title="Tournament Team Check-In", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #013220; color: white; }
    .main-title { color: #ce933e; text-align: center; font-size: 3rem; font-weight: bold; }
    .team-card { 
        background-color: #024f32; padding: 30px; border-radius: 15px; 
        border: 2px solid #ce933e; text-align: center; 
    }
    .gold { color: #ce933e !important; }
    div.stButton > button {
        width: 100%; height: 3.5em; background-color: #ce933e; 
        color: #013220; font-weight: bold; border-radius: 8px;
    }
    /* Simple table styling for the dashboard */
    .styled-table { margin-left: auto; margin-right: auto; border-collapse: collapse; width: 80%; }
    </style>
    """, unsafe_allow_html=True)

# --- Database Connection ---
# Make sure your Google Sheet has headers: team_id, player_name
conn = st.connection("gsheets", type=GSheetsConnection)

def get_live_data():
    return conn.read(ttl=0)

# --- URL Routing ---
params = st.query_params
team_id = params.get("team_id")
is_admin = "admin" in params

# --- 1. THE BIG SCREEN (Admin Dashboard) ---
if is_admin:
    st.markdown("<h1 class='main-title'>🏆 OFFICIAL TOURNAMENT BOARD</h1>", unsafe_allow_html=True)
    
    data = get_live_data()
    
    # We create a display for 20 teams (40 players total, 2 per team)
    teams_list = []
    for i in range(1, 21):
        members = data[data['team_id'] == str(i)]['player_name'].tolist()
        # Fill slots with "Waiting..." if empty
        p1 = members[0] if len(members) > 0 else "⏳ Waiting..."
        p2 = members[1] if len(members) > 1 else "⏳ Waiting..."
        teams_list.append({"Team": f"Team {i}", "Player 1": p1, "Player 2": p2})
    
    st.table(pd.DataFrame(teams_list))
    
    # Auto-refresh helper
    time.sleep(5)
    st.rerun()

# --- 2. THE PLAYER CHECK-IN ---
elif team_id:
    st.markdown(f"<h1 class='main-title'>Welcome to Team {team_id}</h1>", unsafe_allow_html=True)
    
    data = get_live_data()
    # Count how many players are already on this specific team
    current_team = data[data['team_id'] == str(team_id)]
    
    if len(current_team) >= 2:
        st.markdown(f"""
            <div class="team-card">
                <h2 class="gold">Team {team_id} is Full!</h2>
                <p>Confirmed Players: <b>{", ".join(current_team['player_name'].tolist())}</b></p>
            </div>
        """, unsafe_allow_html=True)
    else:
        with st.form("entry_form"):
            st.markdown("<p style='text-align:center;'>Enter your name to join your teammate.</p>", unsafe_allow_html=True)
            name = st.text_input("Full Name", placeholder="e.g. Braden Blagburn")
            submit = st.form_submit_button("LOCK IN MY TEAM")
            
            if submit:
                if name.strip() == "":
                    st.error("Please enter your name.")
                else:
                    # Write to Google Sheets
                    new_entry = pd.DataFrame([{"team_id": str(team_id), "player_name": name}])
                    updated_df = pd.concat([data, new_entry], ignore_index=True)
                    conn.update(data=updated_df)
                    
                    st.balloons()
                    st.success(f"Registered! Look at the main screen, {name}!")
                    time.sleep(2)
                    st.rerun()

# --- 3. FALLBACK ---
else:
    st.markdown("<h1 class='main-title'>⛳ Scanner Active</h1>", unsafe_allow_html=True)
    st.info("Please scan the QR code found inside your team envelope.")
