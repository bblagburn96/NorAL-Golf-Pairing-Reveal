import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time

# --- 1. INITIAL PAGE & THEME CONFIGURATION ---
st.set_page_config(
    page_title="NorAL Golf Tournament Portal",
    page_icon="🏆",
    layout="wide",  # Forces layout to stretch and use full monitor width
    initial_sidebar_state="expanded"
)

# Premium Emerald Golf Theme CSS Styling
st.markdown("""
    <style>
        .main { background-color: #f4f6f4; }
        .stTitle { color: #1b4332; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; font-size: 3rem; }
        .leaderboard-card {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #1b4332;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 12px;
        }
        .team-title { font-size: 1.2rem; font-weight: bold; color: #2d6a4f; }
        .team-score { font-size: 1.5rem; font-weight: 900; color: #1b4332; float: right; }
        .podium-box {
            background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
    </style>
""", unsafe_allow_html=True)


# --- 2. AUTOMATIC VERTICAL SCROLL COMPONENT ---
# Smoothly scrolls desktop monitors down and loops back to the top instantly
auto_scroll_js = """
<script>
    function pageScroll() {
        window.scrollBy(0,1); // Adjust to 2 for faster scrolling speeds
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
            setTimeout(function() {
                window.scrollTo(0,0);
            }, 4000); // Pauses at the bottom for 4 seconds before resetting
        }
        scrolldelay = setTimeout(pageScroll, 35); 
    }
    window.onload = pageScroll;
</script>
"""
components.html(auto_scroll_js, height=0, width=0)


# --- 3. LOCAL DATA MANAGEMENT (NO EXTERNAL DB) ---
# We initialize a dataframe in Streamlit's session state so it remembers data without a Google Sheet
if 'tournament_data' not in st.session_state:
    # Generate teams 1 through 20 (already excluding 21-25 as requested)
    initial_data = {
        'team_id': [i for i in range(1, 21)],
        'Player_1': [f"Player A{i}" for i in range(1, 21)],
        'Player_2': [f"Player B{i}" for i in range(1, 21)],
        'Score': [72] * 20  # Default starting score
    }
    st.session_state.tournament_data = pd.DataFrame(initial_data)

# Load the dataframe from session state
df = st.session_state.tournament_data

# Sort by lowest score first (Standard Gross Stroke Play rules)
df = df.sort_values(by="Score", ascending=True).reset_index(drop=True)


# --- 4. APPLICATION NAVIGATION & PAGES ---
st.sidebar.image("https://img.icons8.com/ios-filled/100/1b4332/golf.png", width=80)
st.sidebar.title("NorAL Navigation")
page = st.sidebar.radio("Go to:", ["Live Leaderboard", "Score Entry", "Local Rules"])


# --- PAGE 1: LIVE LEADERBOARD ---
if page == "Live Leaderboard":
    st.title("🏆 NorAL Invitational Live Leaderboard")
    
    # Render Podium Row (Top 3 Teams)
    if len(df) >= 3:
        st.markdown("### 🥇 Current Leaders")
        p_col1, p_col2, p_col3 = st.columns(3)
        
        with p_col2: # 1st Place Center
            st.markdown(f"""<div class='podium-box' style='background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%);'>
                <h3>🥇 1st Place</h3>
                <h2>{df.loc[0, 'Player_1']} / {df.loc[0, 'Player_2']}</h2>
                <h1>{df.loc[0, 'Score']}</h1>
            </div>""", unsafe_allow_html=True)
            
        with p_col1: # 2nd Place Left
            st.markdown(f"""<div class='podium-box' style='background: linear-gradient(135deg, #b4b4b4 0%, #707070 100%); margin-top: 20px;'>
                <h3>🥈 2nd Place</h3>
                <h4>{df.loc[1, 'Player_1']} / {df.loc[1, 'Player_2']}</h4>
                <h2>{df.loc[1, 'Score']}</h2>
            </div>""", unsafe_allow_html=True)
            
        with p_col3: # 3rd Place Right
            st.markdown(f"""<div class='podium-box' style='background: linear-gradient(135deg, #cd7f32 0%, #8c4c1a 100%); margin-top: 40px;'>
                <h3>🥉 3rd Place</h3>
                <h4>{df.loc[2, 'Player_1']} / {df.loc[2, 'Player_2']}</h4>
                <h2>{df.loc[2, 'Score']}</h2>
            </div>""", unsafe_allow_html=True)
            
        st.markdown("---")

    # --- TWO-COLUMN GRID LAYOUT ---
    st.markdown("### ⛳ Field Standings")
    col1, col2 = st.columns(2)
    
    midpoint = len(df) // 2
    left_field = df.iloc[:midpoint]
    right_field = df.iloc[midpoint:]
    
    # Render Left
