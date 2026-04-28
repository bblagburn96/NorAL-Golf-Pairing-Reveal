import streamlit as st
import random

st.set_page_config(page_title="NorAL Golf Reveal", layout="wide")

# --- THE ROSTER (Individual Players) ---
players = [
    "Stacey Isom", "Steve Mann", "Danny Mann", "Tom Mann", "Andy Mann", 
    "Kevin Serrett", "Matt Paterson", "Phillip Harris", "Wes Patterson", 
    "Andrew Kelley", "Scott Tidmore", "David Hill", "Monty Davis", 
    "Chase Tidmore", "Geoffrey Mann", "Jake Jolly", "Jake Mann", 
    "Lake Graham", "Mark Caldwell", "Nolan Luda", "Trey Hamilton", 
    "Wes Thornhill", "Chris Mann", "Brandon Tidmore", "Dalton Ricroft", 
    "Jon Shepherd", "Kyle Powell", "Josh Mann", "Kyle Young", "Slayde Guess", 
    "Zach Davis", "Blake Jones", "Jordan Brown", "Braden Blagburn", 
    "Grayson Suggs", "Evan Francis", "Hunter McEwen", "Taylor Kyser", 
    "Andrew Hiss", "Camron Mann", "Dakota Creel", "Easton Anderson", 
    "Jack Bishop", "Ryan Davis", "Stacey Isom (2)", "Steve Mann (2)", 
    "Placeholder 1", "Placeholder 2", "Placeholder 3", "Placeholder 4"
]

# --- THE RANDOMIZER ---
# We use the same seed so the results don't change every time the page refreshes
random.seed(20260725)

# 1. Shuffle all individual players
shuffled_players = list(players)
random.shuffle(shuffled_players)

# 2. Create 25 Teams (Pairs)
team_roster = {}
for i in range(0, len(shuffled_players), 2):
    team_num = str((i // 2) + 1)
    team_roster[team_num] = f"{shuffled_players[i]} & {shuffled_players[i+1]}"

# 3. Create Groupings (Two teams per group for the dashboard)
team_numbers = list(team_roster.keys())
# We'll shuffle the team numbers too so Team 1 isn't always in Group 1
random.shuffle(team_numbers)

pairings = []
for i in range(0, len(team_numbers) - 1, 2):
    pairings.append((team_numbers[i], team_numbers[i+1]))

# --- UI LOGIC ---
query_params = st.query_params
team_id = query_params.get("team_id")
is_admin = query_params.get("admin") == "true"

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
    st.title("⛳ NorAL Golf: Random Pairings Dashboard")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    for idx, pair in enumerate(pairings):
        name_1 = team_roster.get(pair[0])
        name_2 = team_roster.get(pair[1])
        
        with col1 if idx < 6 else col2:
            st.markdown(f"""
                <div class='card'>
                    <h3 style='margin:0;'>Group {idx + 1}</h3>
                    <p style='font-size:18px; margin:5px 0;'><b>Team {pair[0]}:</b> {name_1}</p>
                    <p style='font-size:18px; margin:5px 0;'><b>Team {pair[1]}:</b> {name_2}</p>
                </div>
            """, unsafe_allow_html=True)

# --- 2. PLAYER SCAN VIEW ---
elif team_id:
    player_names = team_roster.get(str(team_id), "Guest")
    st.balloons()
    st.markdown(f"""
        <div class='assignment-box'>
            <span style='font-size:24px;'>Envelope Result:</span><br>
            <span class='team-number'>TEAM {team_id}</span>
            <hr style='border-color:#fbbf24;'>
            <span style='font-size:20px;'>Your Randomly Assigned Partner is:</span><br>
            <span style='font-size:32px; font-weight:bold; color:#fbbf24;'>{player_names}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("SEE THE FULL TOURNAMENT FIELD"):
        st.query_params.update(admin="true")
        st.rerun()
else:
    st.title("Welcome to NorAL Golf")
    st.warning("Please scan your envelope QR code to reveal your partner.")
