# ui/theme.py

import streamlit as st


def apply_custom_theme():
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Main app background with purple gradient */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* All containers and cards */
        .element-container, .stMarkdown, div[data-testid="stVerticalBlock"] > div {
            background: transparent !important;
        }
        
        /* Main content area */
        .main .block-container {
            padding: 2rem 3rem;
            max-width: 1400px;
        }
        
        /* Title styling */
        h1 {
            color: #1f2937 !important;
            font-weight: 700 !important;
            font-size: 2.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* All text should be dark by default */
        p, span, label, div {
            color: #1f2937 !important;
        }
        
        /* Exception: JSON viewer text should be light */
        div[data-testid="stJson"] p,
        div[data-testid="stJson"] span,
        div[data-testid="stJson"] label,
        div[data-testid="stJson"] div,
        pre p,
        pre span,
        pre label,
        pre div {
            color: #d4d4d4 !important;
        }
        
        /* Main content text */
        .main .block-container {
            color: #1f2937 !important;
        }
        
        /* Subtitle/description */
        .stApp > header + div p {
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 1.1rem !important;
        }
        
        /* White card containers */
        div[data-testid="column"] > div {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        /* Radio buttons styling */
        div[data-testid="stRadio"] > label {
            color: #1f2937 !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }
        
        div[role="radiogroup"] label {
            background: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            border: 2px solid transparent;
            transition: all 0.3s ease;
            color: #1f2937 !important;
        }
        
        div[role="radiogroup"] label:hover {
            background: #f3f4f6;
            border-color: #6366F1;
        }
        
        /* Selected radio button */
        div[role="radiogroup"] label[data-checked="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            border-color: #667eea;
        }
        
        /* Ensure text inside radio buttons is visible */
        div[role="radiogroup"] label span {
            color: inherit !important;
        }
        
        /* Dark text for unselected, white for selected */
        div[role="radiogroup"] label:not([data-checked="true"]) span {
            color: #1f2937 !important;
        }
        
        div[role="radiogroup"] label[data-checked="true"] span {
            color: white !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* File uploader */
        div[data-testid="stFileUploader"] {
            background: white;
            border: 3px dashed #6366F1;
            border-radius: 8px;
            padding: 0.1rem 0.1rem;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
        }
        
        /* Add cloud icon before file uploader */
        div[data-testid="stFileUploader"]::before {
            font-size: 4rem;
            display: block;
            margin-bottom: 1rem;
            filter: grayscale(100%) brightness(0.7);
        }
        
        div[data-testid="stFileUploader"]:hover {
            border-color: #764ba2;
            background: #f9fafb;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
        }
        
        div[data-testid="stFileUploader"]:hover::before {
            filter: grayscale(0%) brightness(1);
        }
        
        /* File uploader label */
        div[data-testid="stFileUploader"] label {
            color: #1f2937 !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
        }
        
        /* File uploader button */
        div[data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            margin-top: 1rem !important;
        }
        
        /* File uploader section */
        div[data-testid="stFileUploader"] section {
            border: none !important;
            background: transparent !important;
        }
        
        /* File uploader small text */
        div[data-testid="stFileUploader"] small {
            color: #6b7280 !important;
            font-size: 0.95rem !important;
        }
        
        /* Success/Info boxes */
        .stSuccess, .stInfo {
            background: white !important;
            border-radius: 12px !important;
            border-left: 4px solid #10b981 !important;
            padding: 1rem !important;
        }
        
        .stInfo {
            border-left-color: #6366F1 !important;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background: white !important;
            border-right: 1px solid #e5e7eb;
        }
        
        section[data-testid="stSidebar"] > div {
            background: white;
        }
        
        /* Sidebar headers */
        section[data-testid="stSidebar"] h2 {
            color: #1f2937 !important;
            font-weight: 600 !important;
        }
        
        /* Checkboxes */
        div[data-testid="stCheckbox"] label {
            color: #1f2937 !important;
            font-weight: 500 !important;
        }
              /* Expander */
        div[data-testid="stExpander"] {
            background: white;
            border-radius: 20px;
            border: none;
            margin: 1rem 0;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Expander header */
        div[data-testid="stExpander"] summary {
            color: #1f2937 !important;
            font-weight: 600 !important;
            font-size: 1.3rem !important;
        }
        
        /* Expander icon color */
        div[data-testid="stExpander"] svg {
            fill: #6366F1 !important;
        }
        
        /* Force grid layout for defect cards container */
        div[data-testid="stExpander"] > div > div > div {
            display: grid !important;
            grid-template-columns: repeat(5, 1fr) !important;
            gap: 1rem !important;
            margin-top: 1.5rem !important;
        }
        
        /* Individual defect cards - target the column divs */
        div[data-testid="stExpander"] div[data-testid="column"] {
            background: white !important;
            border: 2px solid #6366F1 !important;
            border-left: 4px solid #6366F1 !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.1) !important;
            transition: all 0.3s ease !important;
            min-height: 150px !important;
        }
        
        div[data-testid="stExpander"] div[data-testid="column"]:hover {
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Defect card titles */
        div[data-test# Add this CSS styling section right after your imports and before the Config section
        
        /* Subheaders */
        h2, h3 {
            color: #1f2937 !important;
            font-weight: 600 !important;
        }
        
        /* Images */
        img {
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Spinner */
        div[data-testid="stSpinner"] > div {
            border-top-color: #6366F1 !important;
        }
        
        /* JSON viewer */
        pre {
            background: #1e1e1e !important;
            border-radius: 12px !important;
            border: 1px solid #e5e7eb !important;
            color: #d4d4d4 !important;
        }
        
        /* JSON text color */
        pre code {
            color: #d4d4d4 !important;
        }
        
        /* JSON syntax highlighting */
        pre .token.property {
            color: #9cdcfe !important;
        }
        
        pre .token.string {
            color: #ce9178 !important;
        }
        
        pre .token.number {
            color: #b5cea8 !important;
        }
        
        pre .token.boolean {
            color: #569cd6 !important;
        }
        
        /* Streamlit JSON component */
        div[data-testid="stJson"] {
            background: #1e1e1e !important;
            border-radius: 12px !important;
            padding: 1rem !important;
        }
        
        div[data-testid="stJson"] * {
            color: #d4d4d4 !important;
        }
        
        /* Download button */
        .stDownloadButton > button {
            background: #10b981 !important;
            color: white !important;
        }
        
        /* Markdown text */
        .stMarkdown {
            color: #374151;
        }
    </style>
    """, unsafe_allow_html=True)