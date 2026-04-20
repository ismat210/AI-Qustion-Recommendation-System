import streamlit as st

st.set_page_config(
    page_title="AI Question Recommender",
    layout="wide"
)

# ======================================================
# HEADER
# ======================================================
st.title("📚 AI Question Recommendation System")

st.markdown("""
### 🚀 Workflow
1. Upload a document (PDF / DOCX / Image)
2. System extracts questions automatically
3. AI recommends similar questions
""")

# ======================================================
# SYSTEM STATUS PANEL
# ======================================================
st.subheader("System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("✅ Upload Module Ready")

with col2:
    st.success("🤖 ML Model Ready")

with col3:
    st.success("⚡ Recommendation Engine Ready")

# ======================================================
# NAVIGATION HELP
# ======================================================
st.markdown("---")

st.info("""
👉 Use the sidebar to navigate:
- 📤 Upload File
- 🤖 Get Recommendations
""")

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")
st.caption("Built with FastAPI + Streamlit + ML (TF-IDF + BERT Hybrid)")