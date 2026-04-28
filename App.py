import streamlit as st
import random

st.set_page_config(page_title="NorAL Golf Reveal", layout="wide")

# --- USER ROSTER (Update your names here!) ---
# This dictionary maps the Team ID to the actual Player Names
team_roster = {
    "1": "Player Name 1 & Player Name 2",
    "2": "Player Name 3 & Player Name 4",
    "3": "Player Name 5 & Player Name 6",
    "4": "Player Name 7 & Player Name 8",
    "5": "Team 5 Players",
    "6": "Team 6 Players",
    "7": "Team 7 Players",
    "8": "Team 8 Players",
    "9": "Team 9 Players",
    "10": "Team 10 Players",
    "11": "Team 11 Players",
    "12": "Team 12 Players",
    "13": "Team 13 Players",
    "14": "Team 14 Players",
    "15": "Team 15 Players",
    "16": "Team 16 Players",
    "17": "Team 17 Players",
    "18": "Team 18 Players",
    "19": "Team 19 Players",
    "20": "Team 20 Players",
}

# --- LOGIC ---
query_params = st.query_params
team_id = query_params.get("team_id")
is_admin = query_params.get("admin") == "true"

# Consistent Randomization
teams = list(range(1, 21))
random.seed(20260725) 
random.shuffle(teams)
pairings = [(teams[i], teams[i+1]) for i in range(0, len(teams), 2)]

# --- STYLING ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 4em; font-size: 24px; background-color: #1e3a8a; color: white; font-weight: bold; border-radius: 10px; }
    .assignment-box { padding: 40px; border-radius: 15px; background-color: #1e3a8a; color: #ffffff; text-align: center; border: 4px solid #fbbf24; }
    .team-number { font-size: 80px; color: #fbbf24; font-weight: 900; display: block; }
    .card { background-color: #ffffff; border-left: 8px solid #fbbf24; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ADMIN DASHBOARD ---
if is_admin:
    st.title("⛳ NorAL Golf: Tournament Pairings")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    for idx, pair in enumerate(pairings):
        # Get names from our roster
        names_1 = team_roster.get(str(pair[0]), f"Team {pair[0]}")
        names_2 = team_roster.get(str(pair[1]), f"Team {pair[1]}")
        
        with col1 if idx < 5 else col2:
            st.markdown(f"""
                <div class='card'>
                    <h2 style='margin:0; color:#1e3a8a;'>Group {idx + 1}</h2>
                    <p style='font-size:22px; margin:5px 0;'><b>{names_1}</b></p>
                    <p style='font-size:18px; color:gray; margin:0;'><i>playing with</i></p>
                    <p style='font-size:22px; margin:5px 0;'><b>{names_2}</b></p>
                </div>
            """, unsafe_allow_html=True)

# --- 2. PLAYER SCAN VIEW ---
elif team_id:
    player_names = team_roster.get(str(team_id), f"Team {team_id}")
    st.balloons()
    st.markdown(f"""
        <div class='assignment-box'>
            <span style='font-size:30px;'>Welcome,</span><br>
            <span style='font-size:35px; font-weight:bold;'>{player_names}</span>
            <hr style='border-color:#fbbf24;'>
            <span style='font-size:24px;'>You are:</span>
            <span class='team-number'>TEAM {team_id}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("SEE THE FULL FIELD PAIRINGS"):
        st.query_params.update(admin="true")
        st.rerun()

else:
    st.title("Welcome to NorAL Golf")
    st.warning("Please scan your envelope QR code.")
