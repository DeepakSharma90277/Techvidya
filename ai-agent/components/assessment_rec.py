"""
Assessment Recommendation Component
Generates personalized assessment recommendations
"""

import streamlit as st
from datetime import datetime
from services.recommendation_engine import RecommendationEngine
from services.tavily_service import TavilyService
from config import Config

def render_assessment_recommendations(user_data):
    """
    Render assessment recommendations based on user's courses
    
    Args:
        user_data: User context including enrolled courses
    """
    
    # Initialize recommendation engine
    if 'rec_engine' not in st.session_state:
        st.session_state.rec_engine = RecommendationEngine()
    
    if not user_data or not user_data.get('courses'):
        st.warning("⚠️ No courses found. Please enroll in courses to get recommendations.")
        render_sample_assessments()
        return
    
    # Course selection
    st.subheader("Select Course for Recommendations")
    
    courses = user_data.get('courses', [])
    course_names = [f"{c.get('courseName', 'Unknown Course')}" for c in courses]
    
    selected_course_idx = st.selectbox(
        "Choose a course:",
        range(len(course_names)),
        format_func=lambda x: course_names[x]
    )
    
    selected_course = courses[selected_course_idx]
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        difficulty = st.selectbox(
            "Difficulty Level:",
            ['All'] + Config.DIFFICULTY_LEVELS
        )
    
    with col2:
        assessment_type = st.selectbox(
            "Assessment Type:",
            ['All', 'Quiz', 'Coding Challenge', 'Project', 'MCQ Test']
        )
    
    with col3:
        limit = st.slider(
            "Number of Recommendations:",
            min_value=3,
            max_value=15,
            value=5
        )
    
    # Generate recommendations button
    if st.button("🎯 Generate Recommendations", use_container_width=True):
        generate_recommendations(selected_course, difficulty, assessment_type, limit)
    
    # Display recommendations
    if st.session_state.recommendations:
        st.markdown("---")
        st.subheader("📋 Recommended Assessments")
        
        for idx, rec in enumerate(st.session_state.recommendations, 1):
            render_assessment_card(rec, idx)
    
    # Additional resources section
    st.markdown("---")
    st.subheader("📚 Additional Study Resources")
    
    if st.button("🔍 Find Study Materials"):
        find_study_resources(selected_course)

def generate_recommendations(course, difficulty, assessment_type, limit):
    """
    Generate assessment recommendations using the recommendation engine
    
    Args:
        course: Selected course data
        difficulty: Difficulty filter
        assessment_type: Type of assessment filter
        limit: Maximum number of recommendations
    """
    
    with st.spinner("🔄 Generating personalized recommendations..."):
        try:
            recommendations = st.session_state.rec_engine.generate_recommendations(
                course_name=course.get('courseName', ''),
                course_description=course.get('courseDescription', ''),
                difficulty_filter=difficulty if difficulty != 'All' else None,
                type_filter=assessment_type if assessment_type != 'All' else None,
                limit=limit
            )
            
            st.session_state.recommendations = recommendations
            st.success(f"✅ Generated {len(recommendations)} recommendations!")
            
        except Exception as e:
            st.error(f"❌ Error generating recommendations: {str(e)}")

def render_assessment_card(assessment, index):
    """
    Render an assessment recommendation card
    
    Args:
        assessment: Assessment data dictionary
        index: Card index for display
    """
    
    with st.container():
        st.markdown(
            f'''
            <div class="assessment-card">
                <h3>#{index}. {assessment.get("title", "Assessment")}</h3>
                <p><strong>Type:</strong> {assessment.get("type", "N/A")} | 
                   <strong>Difficulty:</strong> {assessment.get("difficulty", "N/A")} | 
                   <strong>Duration:</strong> {assessment.get("duration", "N/A")}</p>
                <p>{assessment.get("description", "No description available.")}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if assessment.get('link'):
                st.link_button(
                    "🔗 Take Assessment",
                    assessment['link'],
                    use_container_width=True
                )
            else:
                st.button(
                    "🔗 Take Assessment",
                    disabled=True,
                    use_container_width=True,
                    help="Link not available"
                )
        
        with col2:
            if st.button(f"📚 Study Materials", key=f"study_{index}", use_container_width=True):
                show_study_materials(assessment)
        
        with col3:
            if st.button(f"💾 Save", key=f"save_{index}", use_container_width=True):
                save_assessment(assessment)
        
        st.markdown("<br/>", unsafe_allow_html=True)

def show_study_materials(assessment):
    """Find and display study materials for the assessment"""
    
    with st.spinner("🔍 Searching for study materials..."):
        try:
            tavily = TavilyService()
            results = tavily.search(
                query=f"{assessment.get('title')} study materials tutorial",
                max_results=3
            )
            
            if results:
                st.success("Found study resources!")
                for i, result in enumerate(results, 1):
                    st.markdown(f"**{i}. [{result.get('title')}]({result.get('url')})**")
                    st.caption(result.get('content', '')[:150] + "...")
            else:
                st.info("No specific materials found. Try searching online.")
                
        except Exception as e:
            st.error(f"Error searching materials: {str(e)}")

def save_assessment(assessment):
    """Save assessment to user's saved list"""
    
    if 'saved_assessments' not in st.session_state:
        st.session_state.saved_assessments = []
    
    if assessment not in st.session_state.saved_assessments:
        st.session_state.saved_assessments.append(assessment)
        st.success("✅ Assessment saved to your list!")
    else:
        st.info("ℹ️ Assessment already saved.")

def find_study_resources(course):
    """Find additional study resources for the course"""
    
    with st.spinner("🔍 Finding study resources..."):
        try:
            tavily = TavilyService()
            query = f"{course.get('courseName')} complete tutorial guide resources"
            results = tavily.search(query=query, max_results=5)
            
            if results:
                for i, result in enumerate(results, 1):
                    with st.expander(f"📖 {result.get('title', 'Resource')}"):
                        st.write(result.get('content', 'No description available.'))
                        st.link_button(
                            "Visit Resource",
                            result.get('url', '#'),
                            use_container_width=True
                        )
            else:
                st.info("No resources found. Please try a different search.")
                
        except Exception as e:
            st.error(f"Error finding resources: {str(e)}")

def render_sample_assessments():
    """Render sample assessments when no user data is available"""
    
    st.info("📝 Here are some sample assessments:")
    
    sample_assessments = [
        {
            "title": "JavaScript Fundamentals Quiz",
            "type": "MCQ Test",
            "difficulty": "Beginner",
            "duration": "30 mins",
            "description": "Test your knowledge of JavaScript basics including variables, functions, and data types.",
            "link": "https://www.w3schools.com/js/js_quiz.asp"
        },
        {
            "title": "React Hooks Challenge",
            "type": "Coding Challenge",
            "difficulty": "Intermediate",
            "duration": "60 mins",
            "description": "Build a functional component using useState, useEffect, and custom hooks.",
            "link": "https://www.freecodecamp.org/learn"
        },
        {
            "title": "Data Structures Assessment",
            "type": "Quiz",
            "difficulty": "Intermediate",
            "duration": "45 mins",
            "description": "Comprehensive test on arrays, linked lists, stacks, and queues.",
            "link": "https://leetcode.com/"
        }
    ]
    
    st.session_state.recommendations = sample_assessments
    
    for idx, rec in enumerate(sample_assessments, 1):
        render_assessment_card(rec, idx)
