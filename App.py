import streamlit as st
import pandas as pd
import random
import time

# --- Page Configuration ---
st.set_page_config(page_title="Golf Pairing Reveal", page_icon="⛳", layout="centered")

# --- Custom CSS for Master's Aesthetic ---
st.markdown("""
    <style>
    .stApp {
        background-color: #013220;
        color: white;
    }
    div.stButton > button {
        width: 100%;
        height: 3em;
        background-color: #f0f2f6;
        color: #013220;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #ce933e;
    }
    .reveal-card {
        background-color: #024f32;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #ce933e;
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #ce933e !important;
        text-align: center;
    }
    .stSelectbox label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Data Architecture ---
players_data = {
    "Grey Beard": {
        "Tier 1": ["Stacey Isom", "Steve Mann", "Danny Mann", "Tom Mann", "Andy Mann", "Kevin Serrett", "Matt Paterson"],
        "Tier 2": ["Phillip Harris", "Wes Patterson", "Andrew Kelley", "Scott Tidmore", "David Hill", "Monty Davis", "Steve Mann (Other)"]
    },
    "Young Buck": {
        "Tier 1": ["Chase Tidmore", "Geoffrey Mann", "Jake Jolly", "Jake Mann", "Lake Graham", "Mark Caldwell", "Nolan Luda", "Trey Hamilton", "Wes Thornhill", "Chris Mann", "Brandon Tidmore", "Dalton Ricroft", "Jon Shepherd", "Kyle Powell", "Josh Mann", "Placeholder 1"],
        "Tier 2": ["Kyle Young", "Slayde Guess", "Zach Davis", "Blake Jones", "Jordan Brown", "Braden Blagburn", "Grayson Suggs", "Evan Francis", "Hunter McEwen", "Taylor Kyser", "Andrew Hiss", "Camron Mann", "Dakota Creel", "Eastan Anderson", "Jack Bishop", "Ryan Davis"]
    }
}

# --- Randomization Engine (Stable Seed) ---
@st.cache_data
def generate_pairings():
    # Use a fixed seed for stability across refreshes
    random.seed(42)
    all_foursomes = []
    
    # Process both categories
    for category in ["Grey Beard", "Young Buck"]:
        t1 = players_data[category]["Tier 1"].copy()
        t2 = players_data[category]["Tier 2"].copy()
        random.shuffle(t1)
        random.shuffle(t2)
        
        # Create 2-man teams (T1 + T2)
        teams = list(zip(t1, t2))
        
        # Group teams into foursomes (2 teams per foursome)
        for i in range(0, len(teams), 2):
            foursome = teams[i:i+2]
            all_foursomes.append(foursome)
            
    # Assign random unique holes (1-18)
    holes = list(range(1, 19))
    random.shuffle(holes)
    
    final_schedule = []
    for idx, foursome in enumerate(all_foursomes):
        hole = holes[idx % len(holes)]
        final_schedule.append({"teams": foursome, "hole": hole})
        
    return final_schedule

schedule = generate_pairings()

# --- UI Logic ---
st.title("⛳ The Invitation Reveal")
st.subheader("Tournament Pairings & Starting Holes")

# Create a flat list of names for the search box
all_names = []
for cat in players_data:
    for tier in players_data[cat]:
        all_names.extend(players_data[cat][tier])
all_names.sort()

selected_player = st.selectbox("Find your name to see your pairing:", ["Select a Name..."] + all_names)

if selected_player != "Select a Name...":
    if st.button("Reveal My Pairing"):
        with st.spinner("🏆 Shuffling Brackets..."):
            time.sleep(3)
        
        # Find the specific player's group
        user_group = None
        for group in schedule:
            # Check if player is in any of the teams in this group
            for team in group['teams']:
                if selected_player in team:
                    user_group = group
                    user_team = team
                    break
        
        if user_group:
            # Identify Partner
            partner = user_team[1] if user_team[0] == selected_player else user_team[0]
            if partner == "Placeholder 1":
                partner = "TBD - See Director"
            
            # Identify Playing Partners (the other team in the foursome)
            other_teams = [t for t in user_group['teams'] if user_team not in [t]]
            
            st.markdown(f"""
            <div class="reveal-card">
                <h3>Pairing Confirmed</h3>
                <p><strong>Your Partner:</strong><br><span style="font-size: 1.5em;">{partner}</span></p>
                <hr style="border-color: #ce933e;">
                <p><strong>Starting Hole:</strong><br><span style="font-size: 1.5em;">Hole {user_group['hole']}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            if other_teams:
                p1, p2 = other_teams[0]
                st.markdown(f"""
                <div style="background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                    <p style="margin-bottom: 5px;"><strong>Playing Partners:</strong></p>
                    {p1} & {p2}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("You are in a 2-some for this round.")

st.markdown("---")
st.caption("Stable Seed: 42 | Pairing Logic: T1/T2 Weighted Random")
