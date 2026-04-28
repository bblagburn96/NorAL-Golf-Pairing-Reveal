import streamlit as st
import time

# --- Style ---
st.set_page_config(page_title="Tournament Reveal", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #013220; color: white; }
    .gold { color: #ce933e !important; }
    .reveal-card {
        background-color: #024f32; padding: 20px; border-radius: 15px;
        border: 2px solid #ce933e; text-align: center;
    }
    div.stButton > button {
        background-color: #ce933e; color: #013220; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE DATA (Hard-coded) ---
ALL_PLAYERS = sorted([
    "Stacey Isom", "Steve Mann", "Danny Mann", "Tom Mann", "Andy Mann", "Kevin Serrett", "Matt Paterson",
    "Phillip Harris", "Wes Patterson", "Andrew Kelley", "Scott Tidmore", "David Hill", "Monty Davis", "Steve Mann (Other)",
    "Chase Tidmore", "Geoffrey Mann", "Jake Jolly", "Jake Mann", "Lake Graham", "Mark Caldwell", "Nolan Luda", 
    "Trey Hamilton", "Wes Thornhill", "Chris Mann", "Brandon Tidmore", "Dalton Ricroft", "Jon Shepherd", 
    "Kyle Powell", "Josh Mann", "Kyle Young", "Slayde Guess", "Zach Davis", "Blake Jones", "Jordan Brown", 
    "Braden Blagburn", "Grayson Suggs", "Evan Francis", "Hunter McEwen", "Taylor Kyser", "Andrew Hiss", 
    "Camron Mann", "Dakota Creel", "Eastan Anderson", "Jack Bishop", "Ryan Davis", "Placeholder 1"
])

# --- PERMANENT STORAGE (Live Session) ---
# This keeps data in the server's memory while it's running
if 'registration_db' not in st.session_state:
    # Dictionary of {team_id: [list_of_names]}
    st.session_state.registration_db = {str(i): [] for i in range(1, 21)}

# --- URL Logic ---
params = st.query_params
team_id = params.get("team_id")
is_admin = "admin" in params

# --- 1. ADMIN DASHBOARD ---
if is_admin:
    st.markdown("<h1 style='text-align:center;' class='gold'>🏆 LIVE TOURNAMENT BOARD</h1>", unsafe_allow_html=True)
    
    # Create columns for a "Scoreboard" look
    cols = st.columns(2)
    for i in range(1, 21):
        col_idx = 0 if i <= 10 else 1
        with cols[col_idx]:
            names = st.session_state.registration_db[str(i)]
            p1 = names[0] if len(names) > 0 else "---"
            p2 = names[1] if len(names) > 1 else "---"
            st.markdown(f"**Team {i}:** {p1} & {p2}")
    
    time.sleep(2) # Auto-refresh effect
    st.rerun()

# --- 2. PLAYER CHECK-IN ---
elif team_id:
    st.markdown(f"<h1 class='gold'>Team {team_id} Registration</h1>", unsafe_allow_html=True)
    
    current_team = st.session_state.registration_db.get(str(team_id), [])
    
    if len(current_team) >= 2:
        st.success(f"Team {team_id} is locked! Players: {', '.join(current_team)}")
    else:
        # Player picks their name from the pre-set list
        name = st.selectbox("Select your name to join this team:", ["Select..."] + ALL_PLAYERS)
        
        if st.button("LOCK IN ENTRY"):
            if name != "Select...":
                # Check if player is already on another team
                already_reg = any(name in names for names in st.session_state.registration_db.values())
                
                if already_reg:
                    st.error("This name has already been registered!")
                else:
                    st.session_state.registration_db[str(team_id)].append(name)
                    st.balloons()
                    st.success(f"Welcome, {name}! You are confirmed for Team {team_id}.")
                    time.sleep(2)
                    st.rerun()

else:
    st.title("⛳ Welcome")
    st.write("Scan your envelope QR to begin.")
