import streamlit as st
import random

st.set_page_config(page_title="NorAL Golf Reveal", layout="wide")

# --- ACTUAL TOURNAMENT ROSTER ---
team_roster = {
    "1": "Stacey Isom & Steve Mann",
    "2": "Danny Mann & Tom Mann",
    "3": "Andy Mann & Kevin Serrett",
    "4": "Matt Paterson & Phillip Harris",
    "5": "Wes Patterson & Andrew Kelley",
    "6": "Scott Tidmore & David Hill",
    "7": "Monty Davis & Chase Tidmore",
    "8": "Geoffrey Mann & Jake Jolly",
    "9": "Jake Mann & Lake Graham",
    "10": "Mark Caldwell & Nolan Luda",
    "11": "Trey Hamilton & Wes Thornhill",
    "12": "Chris Mann & Brandon Tidmore",
    "13": "Dalton Ricroft & Jon Shepherd",
    "14": "Kyle Powell & Josh Mann",
    "15": "Kyle Young & Slayde Guess",
    "16": "Zach Davis & Blake Jones",
    "17": "Jordan Brown & Braden Blagburn",
    "18": "Grayson Suggs & Evan Francis",
    "19": "Hunter McEwen & Taylor Kyser",
    "20": "Andrew Hiss & Camron Mann",
    "21": "Dakota Creel & Easton Anderson",
    "22": "Jack Bishop & Ryan Davis",
    "23": "Stacey Isom (2) & Steve Mann (2)",
    "24": "Placeholder 1 & Placeholder 2",
    "25": "Placeholder 3 & TBD"
}

# --- LOGIC ---
query_params = st.query_params
team_id = query_params.get("team_id")
is_admin = query_params.get("admin") == "true"

# Shuffle all 25 teams
teams = list(range(1, 26))
random.seed(20260725) 
random.shuffle(teams)

# Create groups of 2 teams (4 players total per group)
pairings = []
for i in range(0, len(teams) - 1, 2):
    pairings.append((teams[i], teams[i+1]))

# Handle the odd team out (Team 25) if necessary
leftover = teams[-1] if len(teams) % 2 != 0 else None

# --- STYLING ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 4em; font-size: 24px; background-color: #1e3a8a; color: white; font-weight: bold; border-radius: 10px; }
    .assignment-box { padding: 40px; border-radius: 15px; background-color: #1e3a8a; color: #ffffff; text-align: center; border: 4px solid #fbbf24; }
    .team-number { font-size: 80px; color: #fbbf24; font-weight: 900; display: block; }
    .card { background-color: #ffffff; border-left: 8px solid #fbbf24; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ADMIN DASHBOARD ---
if is_admin:
    st.title("⛳ NorAL Golf: Tournament Pairings")
    st.write("Each Group represents two teams playing together.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    for idx, pair in enumerate(pairings):
        name_1 = team_roster.get(str(pair[0]))
        name_2 = team_roster.get(str(pair[1]))
        
        with col1 if idx < 6 else col2:
            st.markdown(f"""
                <div class='card'>
                    <h3 style='margin:0;'>Group {idx + 1}</h3>
                    <p style='font-size:18px; margin:5px 0;'><b>Team {pair[0]}:</b> {name_1}</p>
                    <p style='font-size:18px; margin:5px 0;'><b>Team {pair[1]}:</b> {name_2}</p>
                </div>
            """, unsafe_allow_html=True)
            
    if leftover:
        st.warning(f"Note: Team {leftover} ({team_roster.get(str(leftover))}) will be added to a group shortly.")

# --- 2. PLAYER SCAN VIEW ---
elif team_id:
    player_names = team_roster.get(str(team_id), "Guest")
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
