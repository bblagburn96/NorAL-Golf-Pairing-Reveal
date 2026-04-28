import streamlit as st
import random

# Set page config
st.set_page_config(page_title="NorAL Golf Reveal", layout="wide")

# Get URL parameters
query_params = st.query_params
team_id = query_params.get("team_id")
is_admin = query_params.get("admin") == "true"

# --- RANDOM PAIRING LOGIC ---
# Using 20260725 as a seed ensures the "random" shuffle is the 
# same for every person who opens the app on tournament day.
teams = list(range(1, 21))
random.seed(20260725) 
random.shuffle(teams)

# Create pairs from the shuffled list
pairings = []
for i in range(0, len(teams), 2):
    pairings.append((teams[i], teams[i+1]))

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; height: 4em; font-size: 24px; background-color: #1e3a8a; color: white; font-weight: bold; border-radius: 10px; }
    .assignment-box { 
        padding: 40px; border-radius: 15px; background-color: #1e3a8a; 
        color: #ffffff; text-align: center; margin-bottom: 20px; border: 4px solid #fbbf24;
    }
    .team-number { font-size: 80px; color: #fbbf24; font-weight: 900; display: block; }
    .sub-text { font-size: 32px; font-weight: 700; display: block; margin-bottom: 10px; }
    .card { background-color: #f8fafc; border-left: 5px solid #1e3a8a; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ADMIN / TOURNAMENT DASHBOARD VIEW ---
if is_admin:
    st.title("⛳ NorAL Golf: Tournament Dashboard")
    st.subheader("July 25, 2026 | Guntersville State Park")
    st.markdown("---")
    
    st.info("🏆 **Format:** Lowest Total Team Score. All teams play in randomly assigned pairings.")
    
    col1, col2 = st.columns(2)
    
    # Display the 10 random pairings
    for idx, pair in enumerate(pairings):
        with col1 if idx < 5 else col2:
            st.markdown(f"""
                <div class='card'>
                    <h3 style='margin:0;'>Group {idx + 1}</h3>
                    <p style='font-size:20px; margin:0;'>Team {pair[0]} & Team {pair[1]}</p>
                </div>
            """, unsafe_allow_html=True)

# --- 2. PLAYER SCAN VIEW ---
elif team_id:
    st.balloons()
    st.markdown(f"""
        <div class='assignment-box'>
            <span class='sub-text'>You have been assigned to:</span>
            <span class='team-number'>TEAM {team_id}</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### Check the live pairings below to find who you're playing with!")
    
    if st.button("OPEN LIVE DASHBOARD"):
        st.query_params.update(admin="true")
        st.rerun()

# --- 3. DEFAULT LANDING ---
else:
    st.title("Welcome to NorAL Golf")
    st.warning("Please scan the QR code inside your envelope to see your team assignment.")
