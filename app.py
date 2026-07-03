import streamlit as st
from humanizer_engine import RewriterEngine
import time

st.set_page_config(page_title="Stealth Rewriter", page_icon="✍️", layout="wide")

st.markdown("""
<style>
.main-header { font-size: 2.5rem; color: #FF6B35; }
.stButton > button { background: #FF6B35; color: white; }
.stButton > button:hover { background: #E55A2B; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">✍️ Stealth Rewriter</h1>', unsafe_allow_html=True)
st.markdown("*Rewrite sentences while preserving meaning*")

with st.sidebar:
    st.header("⚙️ Settings")
    style = st.selectbox("🎨 Writing Style", ["Natural", "Casual", "Professional", "Creative"])
    st.markdown("---")
    st.info("""
    **How it works:**
    1. Rewrites sentences (not just synonyms)
    2. Changes sentence structure
    3. Active ↔ Passive voice
    4. Cleft sentences
    5. Fronting and inversion
    """)

@st.cache_resource
def load_rewriter():
    return RewriterEngine()

try:
    rewriter = load_rewriter()
    st.success("✅ Rewriter ready!")
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.stop()

input_text = st.text_area("📝 Enter text to rewrite", height=200,
                          placeholder="Paste your text here...")

if st.button("✍️ Rewrite", type="primary") and input_text:
    with st.spinner("Rewriting..."):
        start = time.time()
        result = rewriter.rewrite(input_text, style=style.lower())
        score = rewriter.get_score(result)
        elapsed = time.time() - start
        
        st.success(f"✅ Rewritten in {elapsed:.1f}s!")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("📊 Rewrite Score", f"{score}%")
        with col2: st.metric("📝 Original Words", len(input_text.split()))
        with col3: st.metric("✍️ New Words", len(result.split()))
        
        tab1, tab2 = st.tabs(["✍️ Rewritten Text", "📋 Original"])
        with tab1:
            st.text_area("Rewritten Output", result, height=150)
            st.download_button("📥 Download", result, file_name="rewritten.txt")
        with tab2:
            st.text_area("Original Text", input_text, height=150, disabled=True)
