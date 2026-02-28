"""
Chat Interface Component
Handles the AI study assistant chat functionality
"""

import streamlit as st
from datetime import datetime
from services.llm_service import LLMService
from services.tavily_service import TavilyService
from config import Config

def render_chat_interface(user_data):
    """
    Render the chat interface for AI study assistant
    
    Args:
        user_data: User context data including courses and profile
    """
    
    # Initialize services
    if 'llm_service' not in st.session_state:
        st.session_state.llm_service = LLMService()
    
    if 'tavily_service' not in st.session_state:
        st.session_state.tavily_service = TavilyService()
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                render_message(message)
        else:
            st.info("👋 Hi! I'm your AI study assistant. Ask me anything about your courses or request study materials!")
    
    # Quick action buttons
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 Summarize Course"):
            if user_data and user_data.get('courses'):
                course_name = user_data['courses'][0].get('courseName', 'your course')
                handle_quick_action(f"Provide a comprehensive summary of {course_name}")
    
    with col2:
        if st.button("🎯 Study Tips"):
            handle_quick_action("Give me effective study tips for technical subjects")
    
    with col3:
        if st.button("📝 Practice Problems"):
            handle_quick_action("Suggest practice problems for my current topics")
    
    # Chat input
    st.markdown("---")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_area(
            "Ask a question or request study materials:",
            height=100,
            placeholder="E.g., 'Explain React hooks' or 'Find resources about data structures'",
            key="chat_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_web = st.checkbox("🌐 Search Web", value=True, help="Use Tavily to search for current information")
        send_button = st.button("Send 📤", use_container_width=True)
    
    if send_button and user_input.strip():
        handle_user_message(user_input, user_data, search_web)
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

def handle_user_message(message, user_data, search_web):
    """
    Process user message and generate response
    
    Args:
        message: User's message
        user_data: User context
        search_web: Whether to search web using Tavily
    """
    
    # Add user message to history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': message,
        'timestamp': datetime.now().strftime("%H:%M")
    })
    
    with st.spinner("🤔 Thinking..."):
        try:
            # Get context from user data
            context = build_context(user_data)
            
            # Search web if enabled
            web_results = None
            if search_web:
                web_results = st.session_state.tavily_service.search(
                    query=message,
                    max_results=3
                )
            
            # Generate response
            response = st.session_state.llm_service.generate_response(
                user_message=message,
                context=context,
                web_results=web_results,
                chat_history=st.session_state.chat_history[-10:]  # Last 10 messages
            )
            
            # Add assistant response to history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().strftime("%H:%M"),
                'sources': web_results if web_results else None
            })
            
            # Limit chat history
            if len(st.session_state.chat_history) > Config.MAX_CHAT_HISTORY:
                st.session_state.chat_history = st.session_state.chat_history[-Config.MAX_CHAT_HISTORY:]
        
        except Exception as e:
            st.error(f"❌ Error generating response: {str(e)}")
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': "I apologize, but I encountered an error. Please try again.",
                'timestamp': datetime.now().strftime("%H:%M")
            })

def handle_quick_action(prompt):
    """Handle quick action button clicks"""
    st.session_state.chat_input = prompt
    handle_user_message(prompt, st.session_state.get('user_context'), True)
    st.rerun()

def build_context(user_data):
    """
    Build context string from user data
    
    Args:
        user_data: User context data
        
    Returns:
        str: Formatted context string
    """
    if not user_data:
        return "No user context available."
    
    context_parts = []
    
    if user_data.get('firstName'):
        context_parts.append(f"Student: {user_data.get('firstName')} {user_data.get('lastName', '')}")
    
    if user_data.get('courses'):
        courses = [c.get('courseName', 'Unknown') for c in user_data['courses']]
        context_parts.append(f"Enrolled Courses: {', '.join(courses)}")
    
    return "\n".join(context_parts) if context_parts else "No specific context available."

def render_message(message):
    """
    Render a single chat message
    
    Args:
        message: Message dictionary with role, content, and timestamp
    """
    role = message.get('role', 'user')
    content = message.get('content', '')
    timestamp = message.get('timestamp', '')
    sources = message.get('sources')
    
    if role == 'user':
        st.markdown(
            f'<div class="chat-message user-message">'
            f'<strong>You</strong> <span style="color: #6B7280; font-size: 0.875rem;">{timestamp}</span><br/>'
            f'{content}'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-message assistant-message">'
            f'<strong>🎓 AI Assistant</strong> <span style="color: #6B7280; font-size: 0.875rem;">{timestamp}</span><br/>'
            f'{content}'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Show sources if available
        if sources and isinstance(sources, list):
            with st.expander("📚 Sources"):
                for idx, source in enumerate(sources, 1):
                    st.markdown(f"**{idx}. [{source.get('title', 'Source')}]({source.get('url', '#')})**")
                    st.caption(source.get('content', '')[:200] + "...")
