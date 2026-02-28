"""
Sidebar Component
User authentication and navigation
"""

import streamlit as st
from utils.api_client import APIClient
from config import Config

def render_sidebar():
    """
    Render the sidebar with user authentication and settings
    
    Returns:
        dict: User data if authenticated, None otherwise
    """
    
    with st.sidebar:
        # Logo and branding
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem;">
                <h1 style="color: #4F46E5;">🎓</h1>
                <h2 style="color: #4F46E5; margin: 0;">TechVidya</h2>
                <p style="color: #6B7280; margin: 0;">AI Study Assistant</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # User authentication section
        st.subheader("👤 User Login")
        
        # Check if already logged in
        if st.session_state.get('user_context'):
            user_data = st.session_state.user_context
            
            st.success("✅ Logged In")
            
            st.markdown(f"**Name:** {user_data.get('firstName', '')} {user_data.get('lastName', '')}")
            st.markdown(f"**Email:** {user_data.get('email', 'N/A')}")
            st.markdown(f"**Role:** {user_data.get('accountType', 'N/A')}")
            
            # Get courses count
            courses = user_data.get('courses', [])
            if isinstance(courses, list):
                st.markdown(f"**Courses:** {len(courses)}")
            
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
        else:
            # Show login form
            st.markdown("**Login with your TechVidya account:**")
            
            email = st.text_input(
                "Email:",
                placeholder="your.email@example.com",
                key="login_email"
            )
            
            password = st.text_input(
                "Password:",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            if st.button("🔐 Login", use_container_width=True):
                if email.strip() and password.strip():
                    login_user(email.strip(), password.strip())
                else:
                    st.error("Please enter both email and password")
            
            st.caption("💡 Tip: Login on the main site and click 'AI Assistant' to auto-login here!")
        
        st.markdown("---")
        
        # Settings section
        st.subheader("⚙️ Settings")
        
        # Configuration status
        config_errors = Config.validate_config()
        
        if config_errors:
            st.error("❌ Configuration Issues:")
            for error in config_errors:
                st.caption(f"• {error}")
        else:
            st.success("✅ All APIs Configured")
        
        # Show configuration details in expander
        with st.expander("🔧 Configuration Details"):
            config = Config.get_config_summary()
            st.json(config)
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About"):
            st.markdown("""
                **TechVidya AI Assistant** helps you:
                
                - 📚 Get personalized assessment recommendations
                - 💬 Chat with AI about your studies
                - 🔍 Search for study materials
                - 📊 Track your learning progress
                
                **Powered by:**
                - Tavily API (Web Search)
                - Groq API (AI Chat)
                - Streamlit (UI)
            """)
        
        # Quick links
        st.markdown("---")
        st.subheader("🔗 Quick Links")
        
        if st.button("🏠 Main Platform", use_container_width=True):
            st.markdown("[Go to TechVidya](http://localhost:3000)")
        
        if st.button("📧 Support", use_container_width=True):
            st.info("Contact: support@techvidya.com")
        
        # Return user data
        return st.session_state.get('user_context')

def login_user(email, password):
    """
    Login user with email and password
    
    Args:
        email: User email
        password: User password
    """
    
    with st.spinner("🔄 Logging in..."):
        try:
            api_client = APIClient()
            result = api_client.login(email, password)
            
            if result and result.get('token'):
                # Store token and user data
                st.session_state.token = result.get('token')
                st.session_state.user_context = result.get('user')
                st.session_state.user_id = result.get('user', {}).get('_id')
                
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Login failed. Please check your credentials.")
                
        except Exception as e:
            error_msg = str(e)
            if "Login error" in error_msg or "401" in error_msg:
                st.error("❌ Invalid email or password")
            else:
                st.error(f"❌ Error: {error_msg}")

def load_user_data(user_id):
    """
    Load user data from backend API
    
    Args:
        user_id: User ID to fetch data for
    """
    
    with st.spinner("🔄 Loading user data..."):
        try:
            api_client = APIClient()
            user_data = api_client.get_user_context(user_id)
            
            if user_data:
                st.session_state.user_id = user_id
                st.session_state.user_context = user_data
                st.success("✅ User data loaded successfully!")
                st.rerun()
            else:
                st.error("❌ User not found. Please check your User ID.")
                
        except Exception as e:
            st.error(f"❌ Error loading user data: {str(e)}")
            # For demo purposes, create mock data
            st.warning("Using demo data for testing...")
            create_demo_user_data(user_id)

def create_demo_user_data(user_id):
    """Create demo user data for testing"""
    
    demo_data = {
        'firstName': 'Demo',
        'lastName': 'User',
        'email': 'demo@techvidya.com',
        'accountType': 'Student',
        'courses': [
            {
                'courseName': 'Complete Web Development',
                'courseDescription': 'Learn HTML, CSS, JavaScript, React, and Node.js',
                'progress': 45
            },
            {
                'courseName': 'Data Structures & Algorithms',
                'courseDescription': 'Master DSA concepts and problem solving',
                'progress': 30
            }
        ],
        'completed_assessments': 8,
        'avg_score': 85,
        'streak': 12
    }
    
    st.session_state.user_id = user_id
    st.session_state.user_context = demo_data
    st.rerun()

def logout_user():
    """Logout current user"""
    
    st.session_state.user_id = ""
    st.session_state.user_context = None
    st.session_state.token = None
    st.session_state.chat_history = []
    st.session_state.recommendations = []
    st.success("👋 Logged out successfully!")
    st.rerun()
