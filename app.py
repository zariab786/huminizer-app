import streamlit as st
from humanizer_engine import StealthHumanizer
import time

st.set_page_config(page_title="Stealth Humanizer", page_icon="🕵️", layout="wide")

st.markdown("""
<style>
.main-header { font-size: 2.5rem; color: #FF6B35; }
.stButton > button { background: #FF6B35; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🕵️ Stealth Humanizer</h1>', unsafe_allow_html=True)
st.markdown("*Bypass AI detectors like GPTZero, Turnitin & Originality.ai*")

with st.sidebar:
    style = st.selectbox("🎨 Writing Style", ["Natural", "Casual", "Professional", "Creative"])

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

input_text = st.text_area("📝 Enter text to humanize", height=200)

if st.button("🔄 Humanize", type="primary") and input_text:
    with st.spinner("Processing..."):
        start = time.time()
        result = humanizer.humanize(input_text, style=style.lower())
        score = humanizer.get_stealth_score(result)
        
        st.success(f"✅ Done in {time.time()-start:.1f}s!")
        col1, col2 = st.columns(2)
        with col1: st.metric("📊 Stealth Score", f"{score}%")
        with col2: st.metric("📝 Words", len(result.split()))
        
        st.text_area("📄 Humanized Text", result, height=150)
        st.download_button("📥 Download", result, file_name="humanized.txt")