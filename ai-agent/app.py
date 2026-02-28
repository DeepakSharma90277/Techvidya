"""
AI Assessment Recommendation & Study Assistant
Main Streamlit Application

This application provides:
1. Personalized assessment recommendations based on enrolled courses
2. AI-powered study chat assistant using Tavily for information retrieval
3. Integration with the main Ed-Tech platform
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from components.chat_interface import render_chat_interface
from components.assessment_rec import render_assessment_recommendations
from components.sidebar import render_sidebar
from utils.api_client import get_user_context
from config import Config

# Page configuration
st.set_page_config(
    page_title="TechVidya AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .assessment-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #E0E7FF;
        margin-left: 2rem;
    }
    .assistant-message {
        background-color: #F3F4F6;
        margin-right: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    
    if 'user_context' not in st.session_state:
        st.session_state.user_context = None
    
    if 'llm_initialized' not in st.session_state:
        st.session_state.llm_initialized = False

def main():
    """Main application entry point"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("🎓 TechVidya AI Study Assistant")
    st.markdown("---")
    
    # Render sidebar
    user_data = render_sidebar()
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs([
        "📚 Assessment Recommendations",
        "💬 AI Study Chat",
        "📊 Dashboard"
    ])
    
    with tab1:
        st.header("Personalized Assessment Recommendations")
        st.markdown("Get test recommendations based on your enrolled courses and learning progress.")
        render_assessment_recommendations(user_data)
    
    with tab2:
        st.header("AI Study Assistant")
        st.markdown("Ask questions about your courses or get study materials and resources.")
        render_chat_interface(user_data)
    
    with tab3:
        st.header("Learning Dashboard")
        render_dashboard(user_data)

def render_dashboard(user_data):
    """Render the learning dashboard with metrics"""
    
    if not user_data:
        st.info("👋 Please enter your User ID in the sidebar to view your dashboard.")
        return
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Enrolled Courses",
            value=len(user_data.get('courses', [])),
            delta="Active"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Completed Assessments",
            value=user_data.get('completed_assessments', 0),
            delta="+2 this week"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Average Score",
            value=f"{user_data.get('avg_score', 0)}%",
            delta="+5%"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Study Streak",
            value=f"{user_data.get('streak', 0)} days",
            delta="🔥"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📖 Your Enrolled Courses")
    courses = user_data.get('courses', [])
    
    if courses:
        for idx, course in enumerate(courses):
            with st.expander(f"{idx + 1}. {course.get('courseName', 'Unknown Course')}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Description:** {course.get('courseDescription', 'No description available')}")
                    st.write(f"**Progress:** {course.get('progress', 0)}%")
                with col2:
                    if st.button(f"Get Tests", key=f"test_{idx}"):
                        st.success(f"Generating assessments for {course.get('courseName')}...")
    else:
        st.info("No courses enrolled yet. Enroll in courses to get personalized recommendations!")

if __name__ == "__main__":
    main()
