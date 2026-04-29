import streamlit as st
import time

# --- THE MASTER ROSTERS (Includes placeholders) ---
GREY_BEARDS = [
    "Stacey Isom", "Steve Mann", "Danny Mann", "Tom Mann", "Andy Mann",
    "Kevin Serrett", "Matt Paterson", "Phillip Harris", "Wes Patterson",
    "Andrew Kelley", "Scott Tidmore", "David Hill", "Monty Davis", "Grey Beard Guest"
]

YOUNG_BLOODS = [
    "Chase Tidmore", "Geoffrey Mann", "Jake Jolly", "Jake Mann", "Lake Graham",
    "Mark Caldwell", "Nolan Luda", "Trey Hamilton", "Wes Thornhill", "Chris Mann",
    "Brandon Tidmore", "Dalton Ricroft", "Jon Shepherd", "Kyle Powell", "Josh Mann",
    "Kyle Young", "Slayde Guess", "Zach Davis", "Blake Jones", "Jordan Brown",
    "Braden Blagburn", "Grayson Suggs", "Evan Francis", "Hunter McEwen", "Taylor Kyser",
    "Andrew Hiss", "Camron Mann", "Dakota Creel", "Easton Anderson", "Jack Bishop", "Ryan Davis", "Young Blood Guest"
]

# --- FULL CLUBHOUSE THEME ---
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
    
    .reveal-card {
        background: #065f46;
        border: 2px solid #10b981;
        padding: 30px;
        margin-bottom: 30px;
        border-radius: 8px;
        text-align: center;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    .team-card {
        background: #1f2937;
        border-left: 4px solid #059669; 
        padding: 24px;
        margin-bottom: 16px;
        border-radius: 4px;
        text-align: center;
    }
    
    .foursome-header {
        background: #374151;
        color: #fbbf24;
        padding: 10px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        margin-top: 40px;
    }

    .player-row { font-family: 'Montserrat', sans-serif; font-size: 1.4em; letter-spacing: 1px; }
    .empty-slot { color: #374151; font-weight: 400; }
    .filled-slot { color: #ffffff; font-weight: 700; } 
    
    .stButton>button { 
        background-color: #059669; color: white; font-weight: 700; 
        border-radius: 4px; border: none; width: 100%; height: 3.8em;
        text-transform: uppercase; letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA STORAGE ---
@st.cache_resource
def get_tournament_data():
    return {str(i): {"players": [], "category": None} for i in range(1, 26)}

live_data = get_tournament_data()

if 'reveal_active' not in st.session_state:
    st.session_state['reveal_active'] = False

# --- HELPER LOGIC ---
def get_player_class(name):
    clean = name.strip().lower()
    if any(gb.lower() == clean for gb in GREY_BEARDS): return "Grey Beard"
    if any(yb.lower() == clean for yb in YOUNG_BLOODS): return "Young Blood"
    return None

# --- UI ---
st.markdown("<div class='header-box'><div class='main-title'>NorAL Golf Invitational</div><div class='sub-title'>2026 Team Selection</div></div>", unsafe_allow_html=True)

params = st.query_params
team_id = params.get("team_id")

if team_id:
    # --- REGISTRATION VIEW ---
    team_info = live_data.get(str(team_id))
    st.markdown(f"<h2 style='text-align:center; font-family:Playfair Display;'>Team {team_id} Entry</h2>", unsafe_allow_html=True)
    
    if len(team_info["players"]) >= 2:
        st.warning("Team is full.")
    else:
        name_input = st.text_input("Full Name (from Roster):")
        if st.button("Confirm Entry"):
            p_class = get_player_class(name_input)
            if not p_class:
                st.error("Name not found on official roster.")
            elif team_info["category"] and p_class != team_info["category"]:
                st.error(f"Group Rule: This team is designated for {team_info['category']}s.")
            else:
                live_data[str(team_id)]["players"].append(name_input.strip())
                live_data[str(team_id)]["category"] = p_class
                st.session_state['latest_name'] = name_input
                st.session_state['latest_team'] = team_id
                st.session_state['latest_time'] = time.time()
                st.query_params.clear()
                st.rerun()
else:
    # --- DASHBOARD VIEW ---
    if st.session_state['reveal_active']:
        st.markdown("<h2 style='text-align:center;'>Official Foursomes</h2>", unsafe_allow_html=True)
        for cat in ["Grey Beard", "Young Blood"]:
            teams_of_cat = [tid for tid, val in live_data.items() if val["category"] == cat]
            for i in range(0, len(teams_of_cat), 2):
                t1, t2 = teams_of_cat[i], (teams_of_cat[i+1] if i+1 < len(teams_of_cat) else None)
                st.markdown(f"<div class='foursome-header'>{cat} Group</div>", unsafe_allow_html=True)
                for tid in [t1, t2]:
                    if tid:
                        names = live_data[tid]["players"]
                        p1, p2 = (names[0] if len(names)>0 else "---"), (names[1] if len(names)>1 else "---")
                        st.markdown(f"<div class='team-card'><div class='player-row filled-slot'>{p1} & {p2}</div><div class='sub-title'>Team {tid}</div></div>", unsafe_allow_html=True)
    else:
        # Standard Grid with Top-Pin Reveal
        total = sum(len(t["players"]) for t in live_data.values())
        st.markdown(f"<p style='text-align:center; color:#9ca3af;'>FIELD STATUS: {total} / 46</p>", unsafe_allow_html=True)
        
        if 'latest_time' in st.session_state and time.time() - st.session_state['latest_time'] < 15:
            st.markdown(f"<div class='reveal-card'><div style='font-size: 2em; font-weight: 700;'>{st.session_state['latest_name']}</div><div style='font-style: italic;'>Confirmed for Team {st.session_state['latest_team']}</div></div>", unsafe_allow_html=True)

        for i in range(1, 26):
            info = live_data[str(i)]
            icon = "🧔" if info["category"] == "Grey Beard" else "⚡" if info["category"] == "Young Blood" else "⛳"
            p1 = f"{icon} {info['players'][0]}" if len(info['players']) > 0 else "---"
            p2 = f"{icon} {info['players'][1]}" if len(info['players']) > 1 else "---"
            st.markdown(f"""<div class='team-card'><div class='sub-title'>Team {i}</div><div class='player-row {"filled-slot" if p1 != "---" else "empty-slot"}'>{p1}</div><div style='border-top: 1px solid #374151; width: 20%; margin: 8px auto;'></div><div class='player-row {"filled-slot" if p2 != "---" else "empty-slot"}'>{p2}</div></div>""", unsafe_allow_html=True)

    # --- ADMIN CONTROL ---
    with st.expander("Tournament Director"):
        if st.text_input("Password", type="password") == "noral2026":
            if st.button("ACTIVATE FINAL REVEAL"): st.session_state['reveal_active'] = True; st.rerun()
            if st.button("RESET TO REGISTRATION"): st.session_state['reveal_active'] = False; st.rerun()
            if st.button("RESET ALL DATA"): live_data.update({str(i): {"players": [], "category": None} for i in range(1, 26)}); st.rerun()

    time.sleep(5)
    st.rerun()
