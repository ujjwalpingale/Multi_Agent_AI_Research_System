import streamlit as st
import requests

# Configure the Streamlit page
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-Premium Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Dark Theme & Ambient Background */
    .stApp {
        background-color: #0b0f19;
        background-image: 
            radial-gradient(at 0% 0%, rgba(102, 126, 234, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(118, 75, 162, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(42, 138, 246, 0.1) 0px, transparent 50%);
        color: #e2e8f0;
    }
    
    /* Animated Gradient Title */
    .gradient-text {
        background: linear-gradient(-45deg, #667eea, #764ba2, #2a8af6, #a18cd1);
        background-size: 300% 300%;
        animation: gradient_anim 5s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 4.5rem;
        margin-bottom: 0px;
        padding-bottom: 10px;
        text-align: center;
        letter-spacing: -1.5px;
    }
    
    @keyframes gradient_anim {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtext {
        font-size: 1.3rem;
        text-align: center;
        margin-top: -15px;
        margin-bottom: 50px;
        color: #94a3b8;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Glassmorphism Inputs */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 16px 24px !important;
        font-size: 1.2rem !important;
        color: white !important;
        transition: all 0.3s ease !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.4) !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Premium Button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 14px 32px !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 8px 20px rgba(118, 75, 162, 0.3) !important;
        width: 100% !important;
        margin-top: 10px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 15px 25px rgba(118, 75, 162, 0.5) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Section Headers */
    .report-header {
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 24px;
        border-bottom: 2px solid rgba(118, 75, 162, 0.3);
        padding-bottom: 12px;
        color: #f1f5f9;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        background-color: rgba(255,255,255,0.02) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }
    
    /* Alerts overriding */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    
</style>
""", unsafe_allow_html=True)


import json

# Constants
API_URL = "http://127.0.0.1:8000/research"

# UI Layout
st.markdown('<h1 class="gradient-text">✨ Multi-Agent Research System</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtext">AI-powered research with specialized collaborating agents.</p>', unsafe_allow_html=True)

# Main container for center alignment (Search Bar Area)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    topic = st.text_input("Research Topic", placeholder="e.g., Quantum Computing Advancements in 2024...", label_visibility="collapsed")
    generate_btn = st.button("Generate Research Report")

if generate_btn:
    if not topic.strip():
        st.warning("Please enter a research topic before generating the report.")
    else:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Use columns to center the status container slightly
        status_col1, status_col2, status_col3 = st.columns([1, 4, 1])
        with status_col2:
            status_container = st.status("🤖 Initializing AI Agents...", expanded=True)
        
        report_header_placeholder = st.empty()
        report_placeholder = st.empty()
        
        st.markdown("<br>", unsafe_allow_html=True)
        feedback_header_placeholder = st.empty()
        feedback_info_placeholder = st.empty()
        feedback_placeholder = st.empty()
        
        try:
            response = requests.post(
                API_URL,
                json={"topic": topic},
                stream=True,
                timeout=300
            )
            response.raise_for_status()
            
            report_text = ""
            
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    try:
                        event = json.loads(decoded_line)
                        event_type = event.get("type")
                        data = event.get("data")
                        
                        if event_type == "status":
                            status_container.write(f"➔ {data}")
                        elif event_type == "report_chunk":
                            if not report_text:
                                report_header_placeholder.markdown('<div class="report-header">📄 Research Report</div>', unsafe_allow_html=True)
                            report_text += data
                            report_placeholder.markdown(report_text)
                        elif event_type == "feedback":
                            feedback_header_placeholder.markdown('<div class="report-header" style="font-size: 1.6rem;">📝 Peer Review & Feedback</div>', unsafe_allow_html=True)
                            feedback_info_placeholder.info("The Critic Agent has reviewed the generated report and provided the following constructive feedback:")
                            feedback_placeholder.markdown(data)
                        elif event_type == "done":
                            status_container.update(label="✅ Research completed successfully!", state="complete", expanded=False)
                    except json.JSONDecodeError:
                        continue
                        
        except requests.exceptions.ConnectionError:
            status_container.update(label="❌ Connection Error", state="error")
            st.error("Could not connect to the backend. Please ensure the FastAPI server is running on http://127.0.0.1:8000")
        except Exception as e:
            status_container.update(label="⚠️ Error", state="error")
            st.error(f"An unexpected error occurred: {e}")
