import streamlit as st
from humanizer_engine import StealthHumanizer
import time

st.set_page_config(page_title="Stealth Humanizer", page_icon="🕵️", layout="wide")

st.markdown("""
<style>
.main-header { font-size: 2.5rem; color: #FF6B35; }
.stButton > button { background: #FF6B35; color: white; }
.stButton > button:hover { background: #E55A2B; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🕵️ Stealth Humanizer</h1>', unsafe_allow_html=True)
st.markdown("*Bypass AI detectors like GPTZero, Turnitin & Originality.ai*")

with st.sidebar:
    st.header("⚙️ Settings")
    style = st.selectbox("🎨 Writing Style", ["Natural", "Casual", "Professional", "Creative"])
    st.markdown("---")
    st.info("""
    **How it works:**
    1. Paraphrases text using T5
    2. Adds human-like imperfections
    3. Injects natural fillers
    4. Adjusts sentence structure
    5. Bypasses AI detectors
    """)

@st.cache_resource
def load_humanizer():
    with st.spinner("🔄 Loading AI models... (2-3 minutes)"):
        return StealthHumanizer()

try:
    humanizer = load_humanizer()
    st.success("✅ Models loaded!")
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.stop()

input_text = st.text_area("📝 Enter text to humanize", height=200,
                          placeholder="Paste your AI-generated text here...")

if st.button("🔄 Humanize", type="primary") and input_text:
    with st.spinner("Processing..."):
        start = time.time()
        result = humanizer.humanize(input_text, style=style.lower())
        score = humanizer.get_stealth_score(result)
        
        st.success(f"✅ Done in {time.time()-start:.1f}s!")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("📊 Stealth Score", f"{score}%")
        with col2: st.metric("📝 Original Words", len(input_text.split()))
        with col3: st.metric("✍️ Humanized Words", len(result.split()))
        
        tab1, tab2 = st.tabs(["📄 Humanized Text", "📋 Original"])
        with tab1:
            st.text_area("Humanized Output", result, height=150)
            st.download_button("📥 Download TXT", result, file_name="humanized.txt")
        with tab2:
            st.text_area("Original Text", input_text, height=150, disabled=True)
