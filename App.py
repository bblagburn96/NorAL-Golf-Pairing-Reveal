import streamlit as st
import pandas as pd
import time

# --- CLUBHOUSE THEME & BRANDING ---
st.set_page_config(page_title="NorAL Golf | Live Reveal", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@400;700&display=swap');
    
    .stApp { background-color: #0c1e12; color: #f4f1ea; }
    
    .golf-header {
        font-family: 'Playfair Display', serif; color: #d4af37;
        text-align: center; text-transform: uppercase; letter-spacing: 2px;
        border-bottom: 2px solid #d4af37; padding-bottom: 10px; margin-bottom: 20px;
    }
    
    .team-card {
        background: linear-gradient(145deg, #122b1a, #0c1e12);
        border: 1px solid #d4af37; padding: 15px; margin-bottom: 12px;
        border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        text-align: center;
    }
    
    .player-row { font-family: 'Montserrat', sans-serif; font-size: 1.2em; padding: 8px 0; }
    .empty-slot { color: #2d4a36; font-style: italic; font-size: 0.9em; }
    .filled-slot { color: #ffffff; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    
    .stTextInput>div>div>input { background-color: #f4f1ea; color: #0c1e12; border-radius: 0; font-size: 1.2em; }
    .stButton>button { 
        background-color: #d4af37; color: #0c1e12; font-weight: bold; 
        border-radius: 0; border: none; width: 100%; height: 3.5em;
    }
    .download-btn { text-align: center; margin-top: 50px; opacity: 0.3; }
    .download-btn:hover { opacity: 1.0; }
    </style>
    """, unsafe_allow_html=True)

# --- SHARED MEMORY (The Tournament Brain) ---
@st.cache_resource
def get_tournament_data():
    return {str(i): [] for i in range(1, 26)}

live_data = get_tournament_data()

# --- APP ROUTING ---
params = st.query_params
team_id = params.get("team_id")

# Header appears on all views
st.markdown("<div class='golf-header'><h1>NorAL Golf</h1><p>2026 Invitational Reveal</p></div>", unsafe_allow_html=True)

# --- VIEW 1: PLAYER SIGN-IN (Mobile Card Scan) ---
if team_id:
    st.markdown(f"<h2 style='text-align:center;'>TEAM CARD: {team_id}</h2>", unsafe_allow_html=True)
    
    current_team = live_data.get(str(team_id), [])
    
    if len(current_team) >= 2:
        st.success("Registration Complete.")
        st.markdown(f"<div class='player-row filled-slot'>{current_team[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='player-row filled-slot'>{current_team[1]}</div>", unsafe_allow_html=True)
        if st.button("VIEW ALL PAIRINGS"):
            st.query_params.clear()
            st.rerun()
    else:
        st.write("Please sign in to claim your position on this team.")
        name_entry = st.text_input("FULL NAME", placeholder="Enter your name...", key="reg_input")
        
        if st.button("CONFIRM & JOIN"):
            if name_entry:
                live_data[str(team_id)].append(name_entry.strip().upper())
                st.balloons()
                time.sleep(2)
                st.query_params.clear()
                st.rerun()
            else:
                st.error("Identification required to join team.")

# --- VIEW 2: THE LIVE DASHBOARD (Main View) ---
else:
    st.markdown("<h3 style='text-align:center;'>LIVE FIELD UPDATES</h3>", unsafe_allow_html=True)
    
    # Render 25 Team Cards
    for i in range(1, 26):
        members = live_data[str(i)]
        p1 = members[0] if len(members) > 0 else "AWAITING PLAYER..."
        p2 = members[1] if len(members) > 1 else "AWAITING PLAYER..."
        
        st.markdown(f"""
            <div class='team-card'>
                <div style='color:#d4af37; font-size: 0.8em; font-weight: bold;'>TEAM {i}</div>
                <div class='player-row {"filled-slot" if p1 != "AWAITING PLAYER..." else "empty-slot"}'>{p1}</div>
                <div style='border-top: 1px solid rgba(212,175,55,0.1); width: 30%; margin: 2px auto;'></div>
                <div class='player-row {"filled-slot" if p2 != "AWAITING PLAYER..." else "empty-slot"}'>{p2}</div>
            </div>
        """, unsafe_allow_html=True)

    # --- ADMIN EXPORT (Hidden at the bottom) ---
    st.markdown("<div class='download-btn'>", unsafe_allow_html=True)
    export_list = []
    for t_id, names in live_data.items():
        export_list.append({"Team": t_id, "Player 1": names[0] if len(names)>0 else "", "Player 2": names[1] if len(names)>1 else ""})
    
    df_export = pd.DataFrame(export_list)
    csv = df_export.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download Official Pairing Sheet (CSV)",
        data=csv,
        file_name="NorAL_Golf_2026_Pairings.csv",
        mime="text/csv",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Auto-refresh every 5 seconds
    time.sleep(5)
    st.rerun()
