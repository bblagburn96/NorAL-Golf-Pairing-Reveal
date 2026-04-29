# --- UPDATED DATA & LOGIC ---

GREY_BEARDS = [...] # Same list as before
YOUNG_BLOODS = [...] # Same list as before

def get_player_info(name):
    name_clean = name.strip().lower()
    if any(gb.lower() == name_clean for gb in GREY_BEARDS):
        return {"class": "Grey Beard", "tee": "Yellow"}
    if any(yb.lower() == name_clean for yb in YOUNG_BLOODS):
        return {"class": "Young Blood", "tee": "White"}
    return None

# --- UPDATED REGISTRATION DISPLAY ---
if p_info:
    live_data[str(team_id)]["players"].append(name_input.strip())
    live_data[str(team_id)]["category"] = p_info["class"]
    
    st.success(f"Confirmed: {name_input}")
    st.markdown(f"""
        <div style='background:#374151; padding:15px; border-radius:10px; border-left: 5px solid #fbbf24;'>
            <p style='margin:0; font-weight:700;'>OFFICIAL TEE ASSIGNMENT:</p>
            <h2 style='margin:0; color:#fbbf24;'>{p_info['tee']} TEES</h2>
            <p style='margin:0; font-size:0.8em; color:#9ca3af;'>Grouped with fellow {p_info['class']}s</p>
        </div>
    """, unsafe_allow_html=True)
