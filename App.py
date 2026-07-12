import streamlit as st
import time

# --- FORMAL CLUBHOUSE THEME ---
st.set_page_config(page_title="2026 NorAL Golf Invitational", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@400;700&display=swap');
    
    /* --- KIOSK MODE OVERRIDES --- */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 98% !important; 
    }
    
    .stApp { background-color: #111827; color: #f3f4f6; }
    
    .header-box {
        text-align: center;
        padding: 10px 10px; 
        border-bottom: 2px solid #374151;
        margin-bottom: 15px;
        background: linear-gradient(to bottom, #0f172a, #111827);
    }

    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2em;
        color: #ffffff;
        margin-bottom: 0px;
        font-style: italic;
    }

    .sub-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 4px;
        color: #9ca3af;
    }
    
    /* --- 5x4 GRID LAYOUT FOR BIG SCREENS --- */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr); /* 5 Columns */
        grid-template-rows: repeat(4, 1fr);    /* 4 Rows */
        gap: 15px;
        height: calc(100vh - 160px); /* Stretches to fill the TV perfectly */
    }
    
    .team-card {
        background: #1f2937;
        border: 2px solid #374151; 
        border-radius: 6px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 5px;
    }
    
    /* The Glow Effect for Newly Added Players */
    .team-card.highlight {
        background: #065f46;
        border-color: #10b981;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    .team-label {
        font-family: 'Montserrat', sans-serif;
        color: #9ca3af;
        font-size: 0.8em;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .player-row { font-family: 'Montserrat', sans-serif; font-size: 1.1em; letter-spacing: 1px; }
    .empty-slot { color: #374151; font-weight: 400; }
    .filled-slot { color: #ffffff; font-weight: 700; } 
    
    .stButton>button { 
        background-color: #059669; color: white; font-weight: 700; 
        border-radius: 4px; border: none; width: 100%; height: 3.8em;
        text-transform: uppercase; letter-spacing: 2px;
    }
    
    .stProgress > div > div > div > div { background-color: #059669; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ---
@st.cache_resource
def get_tournament_data():
    return {str(i): [] for i in range(1, 21)} 

live_data = get_tournament_data()

# --- HEADER ---
st.markdown("<div class='header-box'><div class='main-title'>NorAL Golf Invitational</div><div class='sub-title'>2026 Team Selection</div></div>", unsafe_allow_html=True)

# --- NAVIGATION ---
params = st.query_params
team_id = params.get("team_id")

if team_id:
    # --- MOBILE REGISTRATION VIEW ---
    st.markdown("<h2 style='text-align:center; font-family:Playfair Display;'>Official Tournament Entry</h2>", unsafe_allow_html=True)
    
    current_team = live_data.get(str(team_id), [])
    
    if len(current_team) >= 2:
        st.warning(f"Team {team_id} is already full.")
        st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{current_team[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='player-row filled-slot' style='text-align:center;'>{current_team[1]}</div>", unsafe_allow_html=True)
        if st.button("Return to Field"):
            st.query_params.clear()
            st.rerun()
    else:
        st.markdown("<p style='text-align:center; color:#9ca3af;'>Identify yourself to join the field.</p>", unsafe_allow_html=True)
        name_entry = st.text_input("Full Name", placeholder="First & Last Name", key="reg_input", label_visibility="collapsed")
        
        if st.button("Confirm Entry"):
            all_names = [name.lower() for team in live_data.values() for name in team]
            
            if not name_entry:
                st.error("Please enter a name.")
            elif name_entry.lower() in all_names:
                st.error(f"'{name_entry}' is already registered in the field!")
            else:
                live_data[str(team_id)].append(name_entry.strip())
                
                placeholder = st.empty()
                with placeholder.container():
                    st.markdown(f"<h3 style='text-align:center;'>Assigning Team Position...</h3>", unsafe_allow_html=True)
                    pb = st.progress(0)
                    for p in range(100):
                        time.sleep(0.01)
                        pb.progress(p + 1)
                
                placeholder.empty()
                st.toast(f"Welcome to Team {team_id}, {name_entry}!", icon="⛳")
                st.markdown(f"<h2 style='text-align:center; color:#10b981;'>Confirmed: Team {team_id}</h2>", unsafe_allow_html=True)
                
                # Register the time and team so the TV Dashboard knows to flash this box
                st.session_state['latest_team'] = str(team_id)
                st.session_state['latest_time'] = time.time()
                
                time.sleep(2.5)
                st.query_params.clear()
                st.rerun()

else:
    # --- BIG SCREEN DASHBOARD VIEW ---
    
    total_players = sum(len(names) for names in live_data.values())
    progress_val = min(total_players / 40.0, 1.0) 
    
    # Progress Bar
    st.markdown(f"<p style='text-align:center; color:#9ca3af; font-size:0.75em; letter-spacing:2px; margin-bottom:5px;'>FIELD STATUS: {total_players} / 40 REGISTERED</p>", unsafe_allow_html=True)
    st.progress(progress_val)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Determine which team box should be highlighted (if updated in the last 10 seconds)
    highlight_team = None
    if 'latest_time' in st.session_state:
        if time.time() - st.session_state['latest_time'] < 10:
            highlight_team = st.session_state['latest_team']
        else:
            del st.session_state['latest_team']
            del st.session_state['latest_time']

    # Build the 5x4 Grid 
    grid_html = "<div class='grid-container'>"
    
    for i in range(1, 21):
        members = live_data[str(i)]
        p1 = members[0] if len(members) > 0 else "---"
        p2 = members[1] if len(members) > 1 else "---"
        
        c1 = "filled-slot" if p1 != "---" else "empty-slot"
        c2 = "filled-slot" if p2 != "---" else "empty-slot"
        
        # Apply the glow effect if this is the team that was just registered
        box_class = "team-card highlight" if str(i) == highlight_team else "team-card"
        
        grid_html += f"<div class='{box_class}'><div class='team-label'>Team {i}</div><div class='player-row {c1}'>{p1}</div><div style='border-top: 1px solid #374151; width: 40%; margin: 6px auto;'></div><div class='player-row {c2}'>{p2}</div></div>"
        
    grid_html += "</div>"
    
    # Render the entire grid
    st.markdown(grid_html, unsafe_allow_html=True)

    # Invisible auto-refresh loop (checks for new registrations every 3 seconds)
    time.sleep(3)
    st.rerun()
