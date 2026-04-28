import streamlit as st

# Set page config for a clean look
st.set_page_config(page_title="NorAL Golf Reveal", layout="wide")

# Get URL parameters
query_params = st.query_params
team_id = query_params.get("team_id")
is_admin = query_params.get("admin") == "true"

# --- STYLE ---
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; height: 3em; font-size: 20px; background-color: #008CBA; color: white; }
    .team-box { padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC ---

# 1. ADMIN DASHBOARD VIEW
if is_admin:
    st.title("⛳ NorAL Golf Tournament Pairings")
    st.write("Live pairings will appear here as teams check in.")
    
    # Example Table - In the future, we can link this to a Sheet to show real names
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Front Nine Groups")
        for i in range(1, 11):
            st.info(f"Group {i}: Team {i} vs Team {i+10}")
            
    with col2:
        st.subheader("Tournament Status")
        st.success("All systems go for July 25th!")

# 2. PLAYER SCAN VIEW
elif team_id:
    st.balloons()
    st.title("Registration Successful!")
    st.markdown(f"<div class='team-box'><h1>You have been assigned to:</h1><br><h1 style='color:red;'>TEAM {team_id}</h1></div>", unsafe_allow_html=True)
    
    st.write("---")
    st.write("Click below to see the full tournament dashboard and find your partner!")
    
    if st.button("View Live Dashboard"):
        # This redirects them to the admin view on their own phone
        st.query_params.update(admin="true")
        st.rerun()

# 3. DEFAULT LANDING (If they just go to the URL)
else:
    st.title("Welcome to NorAL Golf")
    st.image("https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?auto=format&fit=crop&q=80&w=1000", caption="July 25, 2026")
    st.warning("Please scan the QR code inside your envelope to see your team assignment.")
