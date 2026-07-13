import streamlit as st
import time

# --- CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="NorAL Golf Invitational",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Core UI CSS and Kiosk Overrides
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Montserrat:wght@400;700&display=swap');
    
    /* Kiosk Mode Overrides */
    header {visibility: hidden;} 
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}
    .block-container { padding: 1rem !important; max-width: 98% !important; }
    
    /* App Colors & Typography */
    .stApp { background-color: #111827; color: #f3f4f6; }
    
    .header-box { 
        text-align: center; 
        padding: 10px; 
        border-bottom: 2px solid #374151; 
        margin-bottom: 15px; 
        background: linear-gradient(to bottom, #0f172a, #111827); 
    }
    .main-title { 
        font-family: 'Playfair Display', serif; 
        font-size: 2.4em; 
        color: #ffffff; 
        font-style: italic; 
        margin-bottom: 0px;
    }
    .sub-title { 
        font-family: 'Montserrat', sans-serif; 
        font-size: 0.75em; 
        text-transform: uppercase; 
        letter-spacing: 4px; 
        color: #9ca3af; 
    }
    
    /* Grid System */
    .grid-container { 
        display: grid; 
        grid-template-columns: repeat(5, 1fr); 
        grid-template-rows: repeat(4, 1fr); 
        gap: 15px; 
        height: calc(100vh - 180px); 
    }
    .team-card { 
        background: #1f2937; 
        border: 2px solid #374151; 
        border-radius: 6px; 
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        align-items: center; 
        padding: 5px; 
    }
    
    /* Highlight Animation */
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
    
    /* Typography inside cards */
    .team-label { font-family: 'Montserrat', sans-serif; font-size: 0.8em; color: #9ca3af; text-transform: uppercase; font-weight: bold; margin-bottom: 5px; }
    .player-row { font-family: 'Montserrat', sans-serif; font-size: 1.1em; font-weight: bold; margin: 2px 0; }
    .empty-slot { color: #374151; font-weight: normal; }
    .filled-slot { color: #ffffff; }
    
    /* Buttons and Progress */
    .stButton>button { background-color: #059669; color: white; font-weight: 700; border-radius: 4px; border: none; width: 100%; height: 3.5em; text-transform: uppercase; letter-spacing: 2px; }
    .stProgress > div > div > div > div { background-color: #059669; }
    </style>
""", unsafe_allow_html=True)

# --- DATA MANAGEMENT ---
@st.cache_resource
def get_tournament_data():
    """Initializes and persists the 20-team roster framework across sessions."""
    return {str(i): [] for i in range(1, 21)} 

live_data = get_tournament_data()

# --- FRAGMENTED DASHBOARD LOOP ---
@st.fragment(run_every=3)
def display_dashboard():
    """Renders the 5x4 grid and manages the 3-second silent refresh cycle."""
    total_players = sum(len(names) for names in live_data.values())
    st.markdown(f"<p style='text-align:center; color:#9ca3af; font-size:0.75em; letter-spacing:2px; margin-bottom:5px;'>FIELD STATUS: {total_players} / 40 REGISTERED</p>", unsafe_allow_html=True)
    st.progress(min(total_players / 40.0, 1.0))
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Highlight Logic for New Entries
    highlight_team = st.session_state.get('latest_team')
    if 'latest_time' in st.session_state and (time.time() - st.session_state['latest_time'] > 10):
        del st.session_state['latest_team']
        del st.session_state['latest_time']
        highlight_team = None

    # Render Grid Natively via CSS/HTML
    grid_html = "<div class='grid-container'>"
    for i in range(1, 21):
        members = live_data[str(i)]
        p1 = members[0] if len(members) > 0 else "---"
        p2 = members[1] if len(members) > 1 else "---"
        
        c1 = "filled-slot" if p1 != "---" else "empty-slot"
        c2 = "filled-slot" if p2 != "---" else "empty-slot"
        
        box_class = "team-card highlight" if str(i) == highlight_team else "team-card"
        
        grid_html += f"""
        <div class='{box_class}'>
            <div class='team-label'>Team {i}</div>
            <div class='player-row {c1}'>{p1}</div>
            <div style='border-top: 1px solid #374151; width: 40%; margin: 6px auto;'></div>
            <div class='player-row {c2}'>{p2}</div>
        </div>"""
        
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

# --- MAIN APP LAYOUT ---
st.markdown("""
    <div class='header-box'>
        <div class='main-title'>3rd Annual NorAL Golf Invitational</div>
        <div class='sub-title'>Eagle's Nest Golf Course &bull; July 25, 2026</div>
    </div>
""", unsafe_allow_html=True)

# Check if the user is hitting the registration URL
is_registering = st.query_params.get("register")

if is_registering:
    # --- REGISTRATION VIEW (Mobile) ---
    st.markdown("<h2 style='text-align:center; font-family:Playfair Display;'>Official Tournament Entry</h2>", unsafe_allow_html=True)
    
    total_players = sum(len(names) for names in live_data.values())
    
    if total_players >= 40:
        st.error("The tournament field is currently full (40/40).")
    else:
        st.markdown("<p style='text-align:center; color:#9ca3af;'>Enter your name below to secure your spot in the field.</p>", unsafe_allow_html=True)
        name_entry = st.text_input("Full Name", placeholder="First & Last Name", label_visibility="collapsed")
        
        if st.button("Confirm Entry"):
            all_names = [name.lower() for team in live_data.values() for name in team]
            
            if not name_entry:
                st.error("Please enter a name.")
            elif name_entry.lower() in all_names:
                st.error(f"'{name_entry}' is already registered in the field!")
            else:
                # Find the first available team automatically
                assigned_team = None
                for i in range(1, 21):
                    if len(live_data[str(i)]) < 2:
                        assigned_team = str(i)
                        break
                
                # Lock them in
                live_data[assigned_team].append(name_entry.strip())
                st.session_state.update({
                    'latest_team': assigned_team, 
                    'latest_time': time.time()
                })
                
                # Show them their team number
                st.success(f"Success! You have been assigned to Team {assigned_team}.")
                time.sleep(3) # Pause so they have time to read the message on their phone
                
                # Reset the view
                st.query_params.clear()
                st.rerun()

else:
    # --- DASHBOARD VIEW (Big Screen) ---
    display_dashboard()
    
    # --- ADMIN CONTROLS ---
    st.markdown("---")
    with st.expander("Tournament Director"):
        admin_pass = st.text_input("Passcode", type="password")
        if admin_pass == "noral2026":
            if st.button("Reset Entire Field"):
                live_data.update({str(i): [] for i in range(1, 21)})
                st.success("Field has been reset.")
                time.sleep(1)
                st.rerun()
