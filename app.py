import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from langgraph_workflow.graph_definition import run_newsletter_workflow
from utils.logger import setup_logger

# Setup
st.set_page_config(page_title="AI Newsletter Assistant", layout="wide")
logger = setup_logger("ui_app")

DATA_DIR = Path("data")
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.json"
NEWSLETTER_FILE = DATA_DIR / "cache/newsletter.html"
SETTINGS_FILE = Path("config/settings.py")

# --- Inject Custom CSS ---
def inject_custom_css():
    st.markdown("""
        <style>

        /* ===== LIGHT GREY GLOBAL BACKGROUND ===== */
        body {
            background-color: #eceff3 !important;
        }
        .main {
            background-color: transparent !important;
        }

        /* MODERN HEADER WITH GRADIENT */
        .title-container {
            text-align: center;
            margin-bottom: 45px;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        }
        
        .title-container h1 {
            color: white !important;
            font-size: 48px !important;
            font-weight: 800 !important;
            margin-bottom: 10px !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .title-container p {
            color: rgba(255,255,255,0.95) !important;
            font-size: 20px !important;
            font-weight: 300 !important;
        }

        /* ENHANCED METRIC CARDS */
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            margin-bottom: 20px;
            border: 1px solid rgba(102, 126, 234, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
        }
        
        .metric-card h3 {
            color: #667eea !important;
            font-size: 18px !important;
            font-weight: 600 !important;
            margin-bottom: 15px !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-value {
            font-size: 42px !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-label {
            color: #6c757d;
            font-size: 14px;
            margin-top: 8px;
        }

        /* PRIMARY BUTTON ENHANCEMENT */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            font-weight: 700;
            border-radius: 12px;
            padding: 16px 36px;
            border: none;
            font-size: 16px;
            letter-spacing: 0.5px;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.6);
            transform: translateY(-2px);
        }

        /* INFO BOX STYLING */
        .stAlert {
            border-radius: 15px;
            border-left: 5px solid #667eea;
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }

        /* ===== DARK NEWSLETTER PREVIEW BOX (RESTORED) ===== */
        .preview-box {
            background-color: #0e1117 !important;
            color: white !important;
            padding: 25px;
            border-radius: 14px;
            font-family: 'Segoe UI', sans-serif;
            line-height: 1.6;
            box-shadow: rgba(0,0,0,0.5) 0px 4px 16px;
            margin-top: 20px;
        }

        /* ===== BEAUTIFUL CENTERED TABS ===== */
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center !important;
            display: flex !important;
            gap: 25px !important;
            margin-bottom: 35px !important;
        }

        .stTabs [data-baseweb="tab"] {
            font-size: 16px !important;
            font-weight: 600 !important;
            padding: 14px 30px !important;
            border-radius: 12px !important;
            background-color: #ffffff !important;
            color: #6c757d !important;
            border: 2px solid #e9ecef !important;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
            transform: translateY(-2px);
        }

        .stTabs [data-baseweb="tab"]:hover {
            border-color: #667eea !important;
            background-color: #f8f9fa !important;
            transform: translateY(-2px);
        }
        
        /* FEATURE CARD */
        .feature-card {
            background: white;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 6px 25px rgba(0,0,0,0.06);
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            box-shadow: 0 8px 35px rgba(102, 126, 234, 0.15);
            transform: translateX(5px);
        }
        
        .feature-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .feature-title {
            color: #667eea;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .feature-desc {
            color: #6c757d;
            font-size: 14px;
            line-height: 1.6;
        }
        
        /* STATUS BADGE */
        .status-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        }

        /* INPUT FIELDS */
        .stTextInput>div>div>input {
            border-radius: 12px;
            border: 2px solid #e9ecef;
            padding: 12px 16px;
            transition: all 0.3s ease;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- Helper Functions ---
def get_subscriber_count():
    if SUBSCRIBERS_FILE.exists():
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            subscribers = json.load(f)
        return len(subscribers)
    return 0

def get_last_newsletter_time():
    if NEWSLETTER_FILE.exists():
        modified_time = datetime.fromtimestamp(NEWSLETTER_FILE.stat().st_mtime)
        return modified_time.strftime("%Y-%m-%d %H:%M:%S")
    return "No newsletter generated yet."

def load_newsletter_preview():
    if NEWSLETTER_FILE.exists():
        return NEWSLETTER_FILE.read_text(encoding="utf-8")
    return "<p>No newsletter available yet. Please generate one.</p>"

def update_topic(new_topic):
    settings_path = Path("config/settings.py")
    with open(settings_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(settings_path, "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip().startswith("TOPIC"):
                f.write(f"TOPIC = '{new_topic}'\n")
            else:
                f.write(line)
    st.success(f"✅ Topic updated to '{new_topic}'")

# --- HEADER ---
st.markdown("""
<div class="title-container">
    <h1>⚡ AI Newsletter Assistant</h1>
    <p>Intelligent automation for your daily newsletter distribution</p>
</div>
""", unsafe_allow_html=True)

# --- TABS ---
tabs = st.tabs(["🏠 Dashboard", "📰 Newsletter Preview", "📤 Generate & Send", "⚙️ Configuration"])

# 🏠 HOME OVERVIEW
with tabs[0]:
    # Status Badge
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <span class="status-badge">🟢 System Active</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Total Subscribers</h3>
            <div class="metric-value">{get_subscriber_count()}</div>
            <div class="metric-label">Active recipients in your mailing list</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🕒 Last Generated</h3>
            <div class="metric-value" style="font-size: 24px !important;">{get_last_newsletter_time()}</div>
            <div class="metric-label">Most recent newsletter creation time</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Info Alert with better styling
    st.info("🤖 **Automated Scheduling Active** • Your newsletter is automatically generated and sent every day at 9:00 AM")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("### 🎯 System Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Smart Content Curation</div>
            <div class="feature-desc">AI-powered article discovery and relevance filtering</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✍️</div>
            <div class="feature-title">Intelligent Summaries</div>
            <div class="feature-desc">Automated content summarization and synthesis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📧</div>
            <div class="feature-title">Automated Delivery</div>
            <div class="feature-desc">Scheduled distribution to all subscribers</div>
        </div>
        """, unsafe_allow_html=True)

# 📰 NEWSLETTER PREVIEW (Dark Theme Restored - NO CHANGES)
with tabs[1]:
    st.subheader("📰 Latest Newsletter Preview")

    html_content = load_newsletter_preview()

    styled_html = f"""
    <div class="preview-box">
        {html_content}
    </div>
    """

    st.components.v1.html(styled_html, height=650, scrolling=True)

# 📤 SEND NOW
with tabs[2]:
    st.markdown("### ⚡ Generate & Send Newsletter")
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-desc">
            <strong>Manual Trigger:</strong> Initiate the complete newsletter workflow immediately.
            <br><br>
            <strong>Pipeline Steps:</strong>
            <ol style="margin-top: 10px; color: #6c757d;">
                <li>Fetch latest news articles</li>
                <li>Generate intelligent summaries</li>
                <li>Compose newsletter HTML</li>
                <li>Send to all subscribers</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Newsletter Now", use_container_width=True):
            with st.spinner("⏳ Running newsletter pipeline..."):
                try:
                    result = run_newsletter_workflow()
                    st.success("🎉 Newsletter generated & sent successfully!")
                    st.json(result)
                    logger.info("Manual trigger executed successfully from UI.")
                except Exception as e:
                    st.error(f"❌ Workflow failed: {e}")
                    logger.error(f"Manual trigger failed: {e}")

# 🧠 SETTINGS TAB
with tabs[3]:
    st.markdown("### ⚙️ Configuration Settings")

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📋 Newsletter Topic</div>
        <div class="feature-desc">
            Customize the primary topic for content curation. This determines what articles 
            the system will search for and include in your newsletters.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    current_topic = "Artificial Intelligence"
    settings_path = Path("config/settings.py")

    if settings_path.exists():
        for line in settings_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("TOPIC"):
                current_topic = line.split("=")[1].strip().replace("'", "")

    col1, col2 = st.columns([3, 1])
    with col1:
        new_topic = st.text_input("Newsletter Topic", value=current_topic, label_visibility="collapsed", placeholder="Enter newsletter topic...")
    with col2:
        if st.button("💾 Update Topic", use_container_width=True):
            update_topic(new_topic)



