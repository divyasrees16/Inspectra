# app.py

import streamlit as st
import os
from dotenv import load_dotenv

# UI Modules
from ui.theme import apply_custom_theme
from ui.image_upload import render_image_upload
from ui.realtime import render_realtime
from ui.test_video import render_test_video

# =====================================
# Page Configuration
# =====================================
st.set_page_config(page_title="AI Defect Analysis", layout="wide")
apply_custom_theme()

# Update the title section
st.markdown("""
    <div style='background: white; padding: 2rem 3rem; border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 12px; display: inline-block;'>
                <svg width="40" height="40" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 3H5C3.89543 3 3 3.89543 3 5V9C3 10.1046 3.89543 11 5 11H9C10.1046 11 11 10.1046 11 9V5C11 3.89543 10.1046 3 9 3Z"/>
                    <path d="M9 13H5C3.89543 13 3 13.8954 3 15V19C3 20.1046 3.89543 21 5 21H9C10.1046 21 11 20.1046 11 19V15C11 13.8954 10.1046 13 9 13Z"/>
                    <path d="M19 3H15C13.8954 3 13 3.89543 13 5V9C13 10.1046 13.8954 11 15 11H19C20.1046 11 21 10.1046 21 9V5C21 3.89543 20.1046 3 19 3Z"/>
                    <path d="M19 13H15C13.8954 13 13 13.8954 13 15V19C13 20.1046 13.8954 21 15 21H19C20.1046 21 21 20.1046 21 19V15C21 13.8954 20.1046 13 19 13Z"/>
                </svg>
            </div>
            <div>
                <h1 style='margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem;'>INSPECTRA</h1>
                <p style='margin: 0; color: #6b7280; font-size: 1.1rem;'>AI-Powered Industrial Defect Detection & Analysis</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# =====================================
# Load Environment Variables
# =====================================
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")



# =====================================
# Sidebar Configuration
# =====================================
st.sidebar.header("⚙ Configuration")

show_json = st.sidebar.checkbox(
    "Show JSON Output",
    value=True
)

show_ai_analysis = st.sidebar.checkbox(
    "Show AI Analysis",
    value=True
)

# =====================================
# Mode Selection
# =====================================
analysis_mode = st.radio(
    "Choose Mode",
    [
        "Image Upload",
        "Real-Time Detection",
        "Test Video Detection"
    ]
)

# =====================================
# Route to Selected Mode
# =====================================
if analysis_mode == "Image Upload":
    render_image_upload(show_json, show_ai_analysis)

elif analysis_mode == "Real-Time Detection":
    render_realtime()

elif analysis_mode == "Test Video Detection":
    render_test_video()

# =====================================
# Footer
# =====================================


st.markdown("---")
st.markdown(
    "*Enhanced with AI for intelligent defect analysis and actionable insights.*"
)

with st.expander("ℹ️ Defect Types & Information"):
    st.markdown("""
    **Crease**: A fold or wrinkle in the metal surface, typically caused by improper handling or processing
    
    **Crescent Gap**: A curved gap or opening in the material, often indicating structural weakness
    
    **Inclusion**: Foreign material embedded in the metal, which can compromise structural integrity
    
    **Oil Spot**: Staining or discoloration caused by oil contamination during manufacturing
    
    **Punching Hole**: Unwanted holes created during the punching or forming process
    
    **Rolled Pit**: Small depressions or cavities formed during the rolling process
    
    **Silk Spot**: Surface irregularities with a silk-like appearance, indicating material inconsistency
    
    **Waist Folding**: Folding defects that occur at the waist or narrow sections of the material
    
    **Water Spot**: Staining or corrosion marks caused by water exposure
    
    **Welding Line**: Visible lines or marks from welding operations, which may indicate quality issues
    """)
