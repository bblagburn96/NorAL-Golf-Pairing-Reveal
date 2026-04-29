import streamlit as st
import time

# --- ROSTERS ---
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

# --- THEME ---
st.set_page_config(page_title="2026 NorAL Golf Invitational", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@400;700&display=swap');
    .stApp { background-color: #0f172a; color: #f3f4f6; }
    .header-box { text-align: center; padding: 30px 10px; border-bottom: 2px solid #1e293b; background: #020617; margin-bottom: 25px; }
    .main-title { font-family: 'Playfair Display', serif; font-size: 2.5em; color: #ffffff; font-style: italic; }
    .team-card { background: #1e293b; padding: 20px; margin-bottom: 12px; border-radius: 8px; text-align: center; border: 1px solid #334155; }
    .foursome-header { background: #fbbf24; color: #000; padding: 10px; font-family: 'Montserrat'; font-weight: 700; text-transform: uppercase; text-align: center; margin-top: 25px; border-radius: 4px; }
    .player-name { font-family: 'Montserrat'; font-size: 1.2em; font-weight: 700; color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# --- PERSISTENT STATE ---
@st.cache_resource
def get_tournament_data():
    return {str(i): {"players": [], "category": None} for i in range(1, 26)}

live_data = get_tournament_data()

# We use session_state to track if the Admin has toggled the reveal
if 'reveal_active' not in st.session_state:
    st.session_state['reveal_active'] = False

# --- LOGIC ---
def get_player_class(name):
    clean = name.strip().lower()
    if any(gb.lower() == clean for gb in GREY_BEARDS): return "Grey Beard"
    if any(yb.lower() == clean for yb in YOUNG_BLOODS): return "Young Blood"
    return None

st.markdown("<div class='header-box'><div class='main-title'>NorAL Golf Invitational</div></div>", unsafe_allow_html=True)

params = st.query_params
team_id = params.get("team_id")

if team_id:
    # --- REGISTRATION VIEW ---
    team_info = live_data.get(str(team_id))
    st.markdown(f"<h3 style='text-align:center;'>Team {team_id} Registration</h3>", unsafe_allow_html=True)
    
    if len(team_info["players"]) >= 2:
        st.info("Team Full.")
    else:
        name_input = st.text_input("Full Name:")
        if st.button("Confirm Slot"):
            p_class = get_player_class(name_input)
            if not p_class:
                st.error("Name not on official roster.")
            elif team_info["category"] and p_class != team_info["category"]:
                st.error(f"Cannot mix {p_class} with {team_info['category']}.")
            else:
                live_data[str(team_id)]["players"].append(name_input.strip())
                live_data[str(team_id)]["category"] = p_class
                st.success("Registration Successful!")
                time.sleep(2)
                st.query_params.clear()
                st.rerun()
else:
    # --- DASHBOARD VIEW ---
    
    # 1. CHECK IF REVEAL IS ACTIVE
    if st.session_state['reveal_active']:
        st.markdown("<h2 style='text-align:center; color:#fbbf24;'>Official Foursome Pairings</h2>", unsafe_allow_html=True)
        
        for cat in ["Grey Beard", "Young Blood"]:
            teams_of_cat = [tid for tid, val in live_data.items() if val["category"] == cat]
            for i in range(0, len(teams_of_cat), 2):
                t1, t2 = teams_of_cat[i], (teams_of_cat[i+1] if i+1 < len(teams_of_cat) else None)
                
                st.markdown(f"<div class='foursome-header'>{cat} Group</div>", unsafe_allow_html=True)
                for tid in [t1, t2]:
                    if tid:
                        names = live_data[tid]["players"]
                        p1 = names[0] if len(names) > 0 else "---"
                        p2 = names[1] if len(names) > 1 else "---"
                        st.markdown(f"<div class='team-card'><div class='player-name'>{p1} & {p2}</div><div style='font-size:0.7em; color:#9ca3af;'>Team {tid}</div></div>", unsafe_allow_html=True)
    else:
        # 2. SHOW REGISTRATION GRID
        total = sum(len(t["players"]) for t in live_data.values())
        st.markdown(f"<p style='text-align:center; color:#9ca3af;'>Field Progress: {total} / 46 Registered</p>", unsafe_allow_html=True)
        
        cols = st.columns(2)
        for i in range(1, 26):
            info = live_data[str(i)]
            with cols[i % 2]:
                cat = info["category"] if info["category"] else "Open"
                p1 = info["players"][0] if len(info["players"]) > 0 else "---"
                p2 = info["players"][1] if len(info["players"]) > 1 else "---"
                st.markdown(f"<div class='team-card'><div style='font-size:0.7em; color:#9ca3af;'>{cat}</div><div class='player-name'>{p1}</div><div class='player-name'>{p2}</div><div style='font-size:0.7em; color:#9ca3af;'>Team {i}</div></div>", unsafe_allow_html=True)

    # --- ADMIN CONTROL PANEL ---
    with st.expander("Tournament Director Login"):
        pwd = st.text_input("Admin Password", type="password")
        if pwd == "noral2026":
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🚀 ACTIVATE FINAL REVEAL"):
                    st.session_state['reveal_active'] = True
                    st.rerun()
            with col_b:
                if st.button("🔄 BACK TO REGISTRATION"):
                    st.session_state['reveal_active'] = False
                    st.rerun()
            
            if st.button("⛔ EMERGENCY RESET ENTIRE FIELD"):
                live_data.update({str(i): {"players": [], "category": None} for i in range(1, 26)})
                st.session_state['reveal_active'] = False
                st.rerun()

    # iPad Refresh Loop
    time.sleep(5)
    st.rerun()
