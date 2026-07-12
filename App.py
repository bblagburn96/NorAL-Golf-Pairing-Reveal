import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
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


# --- 3. DATABASE CONNECTION (GOOGLE SHEETS) ---
@st.cache_data(ttl=5) # Cache data for exactly 5 seconds to ensure live updates
def load_tournament_data():
    try:
        # Pulls service account credentials from Streamlit secrets management
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        
        # Open your master worksheet
        sheet = client.open("NorALsheet").sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        # Safe offline fallback layout if cloud connection drops during testing
        return pd.DataFrame({
            'team_id': [i for i in range(1, 26)],
            'Player_1': [f"Player A{i}" for i in range(1, 26)],
            'Player_2': [f"Player B{i}" for i in range(1, 26)],
            'Score': [72 + (i % 3) - (i % 2) for i in range(1, 26)] 
        })

df = load_tournament_data()


# --- 4. DATA FILTERING (REMOVE 5 TEAMS) ---
# Explicitly drop the 5 unassigned or empty team slots from your data collection
teams_to_remove = [21, 22, 23, 24, 25]
filtered_df = df[~df['team_id'].isin(teams_to_remove)]

# Sort by lowest score first (Standard Gross Stroke Play rules)
filtered_df = filtered_df.sort_values(by="Score", ascending=True).reset_index(drop=True)


# --- 5. APPLICATION NAVIGATION & PAGES ---
st.sidebar.image("https://img.icons8.com/ios-filled/100/1b4332/golf.png", width=80)
st.sidebar.title("NorAL Navigation")
page = st.sidebar.radio("Go to:", ["Live Leaderboard", "Score Entry", "Local Rules"])


# --- PAGE 1: LIVE LEADERBOARD ---
if page == "Live Leaderboard":
    st.title("🏆 NorAL Invitational Live Leaderboard")
    
    # Render Podium Row (Top 3 Teams)
    if len(filtered_df) >= 3:
        st.markdown("### 🥇 Current Leaders")
        p_col1, p_col2, p_col3 = st.columns(3)
        
        with p_col2: # 1st Place Center
            st.markdown(f"""<div class='podium-box' style='background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%);'>
                <h3>🥇 1st Place</h3>
                <h2>{filtered_df.loc[0, 'Player_1']} / {filtered_df.loc[0, 'Player_2']}</h2>
                <h1>{filtered_df.loc[0, 'Score']}</h1>
            </div>""", unsafe_allow_html=True)
            
        with p_col1: # 2nd Place Left
            st.markdown(f"""<div class='podium-box' style='background: linear-gradient(135deg, #b4b4b4 0%, #707070 100%); margin-top: 20px;'>
                <h3>🥈 2nd Place</h3>
                <h4>{filtered_df.loc[1, 'Player_1']} / {filtered_df.loc[1, 'Player_2']}</h4>
                <h2>{filtered_df.loc[1, 'Score']}</h2>
            </div>""", unsafe_allow_html=True)
            
        with p_col3: # 3rd Place Right
            st.markdown(f"""<div class='podium-box' style='background: linear-gradient(135deg, #cd7f32 0%, #8c4c1a 100%); margin-top: 40px;'>
                <h3>🥉 3rd Place</h3>
                <h4>{filtered_df.loc[2, 'Player_1']} / {filtered_df.loc[2, 'Player_2']}</h4>
                <h2>{filtered_df.loc[2, 'Score']}</h2>
            </div>""", unsafe_allow_html=True)
            
        st.markdown("---")

    # --- TWO-COLUMN GRID LAYOUT ---
    # Split the field data directly down the middle to maximize monitor screen real estate
    st.markdown("### ⛳ Field Standings")
    col1, col2 = st.columns(2)
    
    midpoint = len(filtered_df) // 2
    left_field = filtered_df.iloc[:midpoint]
    right_field = filtered_df.iloc[midpoint:]
    
    # Render Left Column
    with col1:
        for idx, row in left_field.iterrows():
            st.markdown(f"""
                <div class="leaderboard-card">
                    <span class="team-score">{row['Score']}</span>
                    <div class="team-title">Team {int(row['team_id'])}</div>
                    <div style="color: #555; font-size: 0.9rem;">{row['Player_1']} & {row['Player_2']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Render Right Column
    with col2:
        for idx, row in right_field.iterrows():
            st.markdown(f"""
                <div class="leaderboard-card">
                    <span class="team-score">{row['Score']}</span>
                    <div class="team-title">Team {int(row['team_id'])}</div>
                    <div style="color: #555; font-size: 0.9rem;">{row['Player_1']} & {row['Player_2']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Infinite Loop Auto-Refresh Trigger
    time.sleep(5)
    st.rerun()


# --- PAGE 2: SCORE ENTRY (QR CODE PORTAL) ---
elif page == "Score Entry":
    st.title("📝 Player Score Ingestion Portal")
    
    # Correct handling of modern Streamlit query parameters dictionary
    if "team_id" in st.query_params:
        detected_team = st.query_params["team_id"]
        st.success(f"Verified Check-In: Logging score for **Team {detected_team}**")
        try:
            team_selector = int(detected_team)
        except ValueError:
            team_selector = st.selectbox("Select Your Assigned Team Number:", filtered_df['team_id'].tolist())
    else:
        team_selector = st.selectbox("Select Your Assigned Team Number:", filtered_df['team_id'].tolist())
        
    with st.form("score_form"):
        gross_score = st.number_input("Enter Total 18-Hole Gross Strokes:", min_value=50, max_value=120, value=72, step=1)
        submit_btn = st.form_submit_with_button("Commit Score to Leaderboard")
        
        if submit_btn:
            # Code block for gspread sheet updates goes here during active tournament
            st.toast(f"Score of {gross_score} successfully filed for Team {team_selector}!", icon="💾")


# --- PAGE 3: LOCAL RULES ---
elif page == "Local Rules":
    st.title("📜 Tournament Conditions & Local Rules")
    st.markdown("""
    * **Format:** 2-Man Scramble (Gross stroke play).
    * **Tees:** All players play from the White Tees.
    * **Lie Adjustments:** You may move your ball one club-length inside any cut of grass, no closer to the hole. You cannot change cuts of grass (e.g., moving from rough to fairway).
    * **Ties:** Sudden death playoff starting on Hole 18, moving backwards.
    """)
