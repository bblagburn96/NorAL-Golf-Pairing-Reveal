import streamlit as st
import time
import random

# --- CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="NorAL Golf Invitational",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@400;700&display=swap');
    
    /* Global Overrides */
    header {visibility: hidden;} #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .block-container { padding: 1rem !important; max-width: 98% !important; }
    .stApp { background-color: #111827; color: #f3f4f6; }
    
    /* Header Typography */
    .header-box { text-align: center; padding: 15px; border-bottom: 2px solid #374151; margin-bottom: 20px; background: linear-gradient(to bottom, #0f172a, #111827); }
    .main-title { font-family: 'Playfair Display', serif; font-size: 2.8em; color: #ffffff; font-style: italic; margin-bottom: 0px; line-height: 1.1; }
    .sub-title { font-family: 'Montserrat', sans-serif; font-size: 0.85em; text-transform: uppercase; letter-spacing: 4px; color: #10b981; margin-top: 5px; }
    
    /* Responsive Grid System (Works on TV and Mobile) */
    .dynamic-grid { 
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
        gap: 15px; 
    }
    
    /* Cards and Slots */
    .card { background: #1f2937; border: 1px solid #374151; border-radius: 8px; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); }
    .team-label { font-family: 'Montserrat', sans-serif; font-size: 0.85em; color: #9ca3af; text-transform: uppercase; font-weight: bold; margin-bottom: 10px; letter-spacing: 1px; }
    .player-name { font-family: 'Montserrat', sans-serif; font-size: 1.2em; font-weight: bold; color: #ffffff; margin: 4px 0; }
    
    /* Unified Pool Styling */
    .pool-slot { background: #1f2937; border: 1px dashed #374151; border-radius: 4px; padding: 10px; text-align: center; font-family: 'Montserrat', sans-serif; font-weight: bold; }
    .pool-slot.filled { border: 1px solid #10b981; color: #ffffff; background: #064e3b; }
    .pool-slot.empty { color: #4b5563; }
    
    /* Forms & Buttons */
    .stTextInput>div>div>input { background-color: #1f2937; color: white; border: 1px solid #374151; border-radius: 6px; padding: 12px; font-size: 1.1em; }
    .stButton>button { background-color: #10b981; color: #111827; font-weight: 700; border-radius: 6px; border: none; width: 100%; height: 3.5em; text-transform: uppercase; letter-spacing: 2px; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #059669; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- GLOBAL DATA STATE ---
@st.cache_resource
def get_tournament_state():
    """Manages the lifecycle from single pool registration to paired teams."""
    return {
        "players": [],       # The single, unified player pool (up to 40)
        "teams": {},         # Dictionary of 20 teams (empty until generated)
        "status": "open"     # Modes: 'open' (registering) or 'paired' (reveal)
    }

state = get_tournament_state()

# --- LIVE DASHBOARD FRAGMENT ---
@st.fragment(run_every=3)
def display_dashboard():
    """Silently refreshes the display without reloading the browser."""
    
    if state["status"] == "open":
        # PHASE 1: THE UNIFIED POOL
        st.markdown(f"<p style='text-align:center; color:#9ca3af; font-size:0.85em; letter-spacing:3px;'>LIVE UNIFIED PLAYER POOL: {len(state['players'])} / 40</p>", unsafe_allow_html=True)
        st.progress(min(len(state['players']) / 40.0, 1.0))
        st.markdown("<br>", unsafe_allow_html=True)
        
        grid_html = "<div class='dynamic-grid'>"
        for i in range(40):
            if i < len(state["players"]):
                grid_html += f"<div class='pool-slot filled'>{state['players'][i]}</div>"
            else:
                grid_html += f"<div class='pool-slot empty'>Slot {i+1}</div>"
        grid_html += "</div>"
        st.markdown(grid_html, unsafe_allow_html=True)

    elif state["status"] == "paired":
        # PHASE 2: THE OFFICIAL PAIRINGS
        st.markdown("<p style='text-align:center; color:#10b981; font-size:0.85em; letter-spacing:3px; font-weight:bold;'>OFFICIAL TOURNAMENT PAIRINGS LOCKED</p><br>", unsafe_allow_html=True)
        
        grid_html = "<div class='dynamic-grid'>"
        for i in range(1, 21):
            team_members = state["teams"].get(str(i), [])
            p1 = team_members[0] if len(team_members) > 0 else "---"
            p2 = team_members[1] if len(team_members) > 1 else "---"
            
            grid_html += f"""
            <div class='card'>
                <div class='team-label'>Team {i}</div>
                <div class='player-name'>{p1}</div>
                <div style='border-top: 1px solid #374151; width: 60%; margin: 8px auto;'></div>
                <div class='player-name'>{p2}</div>
            </div>"""
        grid_html += "</div>"
        st.markdown(grid_html, unsafe_allow_html=True)

# --- MAIN APPLICATION ROUTING ---
st.markdown("""
    <div class='header-box'>
        <div class='main-title'>3rd Annual NorAL Golf Invitational</div>
        <div class='sub-title'>Eagle's Nest &bull; July 25, 2026</div>
    </div>
""", unsafe_allow_html=True)

# Check if user is accessing via the mobile QR code
is_mobile_entry = st.query_params.get("register")

if is_mobile_entry:
    # --- MOBILE REGISTRATION VIEW ---
    if state["status"] == "paired":
        st.error("Registration is closed. The field has been locked and paired.")
        if st.button("View Live Dashboard"):
            st.query_params.clear()
            st.rerun()
            
    elif len(state["players"]) >= 40:
        st.error("The tournament field is currently full (40/40).")
        if st.button("View Live Dashboard"):
            st.query_params.clear()
            st.rerun()
            
    else:
        st.markdown("<h3 style='text-align:center; font-family:Playfair Display; margin-bottom: 5px;'>Player Entry</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#9ca3af; margin-bottom: 25px;'>Enter your name to join the unified tournament pool.</p>", unsafe_allow_html=True)
        
        # Centered form container for better mobile UX
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            name_entry = st.text_input("Full Name", placeholder="First & Last Name", label_visibility="collapsed")
            
            if st.button("Secure My Spot"):
                clean_name = name_entry.strip()
                existing_names = [n.lower() for n in state["players"]]
                
                if not clean_name:
                    st.error("Please enter a valid name.")
                elif clean_name.lower() in existing_names:
                    st.error(f"'{clean_name}' is already in the player pool!")
                else:
                    state["players"].append(clean_name)
                    st.success("Spot secured! Sending you to the live dashboard...")
                    time.sleep(2.5) # Allow player to read success message
                    st.query_params.clear() # Route them to the dashboard
                    st.rerun()

else:
    # --- KIOSK / MAIN DASHBOARD VIEW ---
    display_dashboard()
    
    # --- TOURNAMENT DIRECTOR CONTROLS ---
    st.markdown("---")
    with st.expander("Tournament Director Operations"):
        admin_pass = st.text_input("Passcode", type="password", key="admin_auth")
        
        if admin_pass == "noral2026":
            colA, colB = st.columns(2)
            
            with colA:
                if state["status"] == "open":
                    if st.button("Lock Field & Generate Pairings"):
                        # Execute pairing logic from the unified pool
                        pool = state["players"].copy()
                        random.shuffle(pool) # Baseline randomization
                        
                        # Distribute into 20 teams of 2
                        new_teams = {str(i): [] for i in range(1, 21)}
                        team_index = 1
                        for player in pool:
                            new_teams[str(team_index)].append(player)
                            if len(new_teams[str(team_index)]) == 2:
                                team_index += 1
                                
                        state["teams"] = new_teams
                        state["status"] = "paired"
                        st.rerun()
                else:
                    st.info("Field is locked and paired.")
                    
            with colB:
                if st.button("Factory Reset (Clear All Data)", type="primary"):
                    state["players"] = []
                    state["teams"] = {}
                    state["status"] = "open"
                    st.rerun()
