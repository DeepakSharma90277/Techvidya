"""
Recommendation Engine
Generates personalized assessment recommendations
"""

from typing import List, Dict, Optional
import random
from services.llm_service import LLMService
from services.tavily_service import TavilyService
from config import Config

class RecommendationEngine:
    """Engine for generating personalized assessment recommendations"""
    
    def __init__(self):
        """Initialize the recommendation engine"""
        self.llm_service = LLMService()
        self.tavily_service = TavilyService()
    
    def generate_recommendations(
        self,
        course_name: str,
        course_description: str = "",
        difficulty_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Generate personalized assessment recommendations
        
        Args:
            course_name: Name of the course
            course_description: Description of the course
            difficulty_filter: Filter by difficulty level
            type_filter: Filter by assessment type
            limit: Maximum number of recommendations
            
        Returns:
            List of assessment recommendations
        """
        
        # Determine difficulty level
        difficulty = difficulty_filter or "Intermediate"
        
        # First, try to use LLM to generate recommendations
        llm_recommendations = self.llm_service.generate_assessment_recommendations(
            course_name=course_name,
            course_description=course_description,
            difficulty=difficulty,
            count=limit
        )
        
        # If LLM recommendations are valid, use them
        if llm_recommendations and len(llm_recommendations) > 0:
            recommendations = self._format_llm_recommendations(
                llm_recommendations,
                course_name,
                difficulty
            )
        else:
            # Fallback to template-based recommendations
            recommendations = self._generate_template_recommendations(
                course_name,
                course_description,
                difficulty,
                limit
            )
        
        # Search for real assessment links using Tavily
        recommendations = self._enrich_with_real_links(recommendations, course_name)
        
        # Apply filters
        if type_filter:
            recommendations = [r for r in recommendations if r['type'] == type_filter]
        
        # Limit results
        return recommendations[:limit]
    
    def _format_llm_recommendations(
        self,
        llm_recs: List[Dict],
        course_name: str,
        difficulty: str
    ) -> List[Dict]:
        """Format LLM-generated recommendations"""
        
        formatted = []
        
        for rec in llm_recs:
            formatted.append({
                'title': rec.get('title', 'Assessment'),
                'type': rec.get('type', 'Quiz'),
                'difficulty': difficulty,
                'duration': rec.get('duration', '30 mins'),
                'description': rec.get('description', ''),
                'topics': rec.get('topics', []),
                'link': '',  # Will be enriched with Tavily
                'course': course_name
            })
        
        return formatted
    
    def _generate_template_recommendations(
        self,
        course_name: str,
        course_description: str,
        difficulty: str,
        limit: int
    ) -> List[Dict]:
        """Generate recommendations using templates (fallback)"""
        
        # Assessment templates based on common topics
        templates = [
            {
                'title_template': '{course} Fundamentals Quiz',
                'type': 'MCQ Test',
                'duration': '30 mins',
                'description': 'Test your understanding of the core concepts and fundamentals of {course}.'
            },
            {
                'title_template': '{course} Coding Challenge',
                'type': 'Coding Challenge',
                'duration': '60 mins',
                'description': 'Apply your {course} knowledge to solve real-world coding problems.'
            },
            {
                'title_template': 'Advanced {course} Assessment',
                'type': 'Quiz',
                'duration': '45 mins',
                'description': 'Deep dive into advanced topics and best practices in {course}.'
            },
            {
                'title_template': '{course} Project Challenge',
                'type': 'Project',
                'duration': '120 mins',
                'description': 'Build a complete project demonstrating your {course} skills.'
            },
            {
                'title_template': '{course} Practice Test',
                'type': 'MCQ Test',
                'duration': '40 mins',
                'description': 'Comprehensive practice test covering all major topics in {course}.'
            },
            {
                'title_template': '{course} Debug Challenge',
                'type': 'Coding Challenge',
                'duration': '50 mins',
                'description': 'Find and fix bugs in {course} code to improve your debugging skills.'
            },
            {
                'title_template': '{course} Interview Prep',
                'type': 'Quiz',
                'duration': '60 mins',
                'description': 'Prepare for technical interviews with {course} questions.'
            },
            {
                'title_template': '{course} Mini Project',
                'type': 'Project',
                'duration': '90 mins',
                'description': 'Create a mini project to demonstrate your understanding of {course}.'
            }
        ]
        
        recommendations = []
        selected_templates = random.sample(templates, min(limit, len(templates)))
        
        for template in selected_templates:
            recommendations.append({
                'title': template['title_template'].format(course=course_name),
                'type': template['type'],
                'difficulty': difficulty,
                'duration': template['duration'],
                'description': template['description'].format(course=course_name),
                'topics': self._extract_topics(course_name),
                'link': '',
                'course': course_name
            })
        
        return recommendations
    
    def _enrich_with_real_links(
        self,
        recommendations: List[Dict],
        course_name: str
    ) -> List[Dict]:
        """Enrich recommendations with real assessment links from Tavily"""
        
        try:
            # Search for assessment resources
            search_results = self.tavily_service.search_assessment_resources(
                course_name=course_name,
                difficulty="intermediate"
            )
            
            # Map search results to recommendations
            for i, rec in enumerate(recommendations):
                if i < len(search_results):
                    rec['link'] = search_results[i].get('url', '')
                else:
                    # Use generic search for remaining recommendations
                    rec['link'] = self._get_generic_assessment_link(rec['type'])
            
        except Exception as e:
            # If Tavily fails, use generic links
            for rec in recommendations:
                rec['link'] = self._get_generic_assessment_link(rec['type'])
        
        return recommendations
    
    def _get_generic_assessment_link(self, assessment_type: str) -> str:
        """Get generic assessment link based on type"""
        
        generic_links = {
            'MCQ Test': 'https://www.w3schools.com/quiztest/',
            'Coding Challenge': 'https://leetcode.com/problemset/',
            'Project': 'https://www.freecodecamp.org/learn',
            'Quiz': 'https://www.geeksforgeeks.org/quiz-corner-gq/'
        }
        
        return generic_links.get(assessment_type, 'https://www.freecodecamp.org/')
    
    def _extract_topics(self, course_name: str) -> List[str]:
        """Extract potential topics from course name"""
        
        # This is a simple extraction - could be enhanced with NLP
        topics = []
        
        keywords = course_name.lower().split()
        
        topic_mapping = {
            'web': ['HTML', 'CSS', 'JavaScript'],
            'python': ['Variables', 'Functions', 'OOP'],
            'java': ['Classes', 'Objects', 'Inheritance'],
            'react': ['Components', 'Hooks', 'State Management'],
            'node': ['Express', 'APIs', 'Middleware'],
            'data': ['Arrays', 'Linked Lists', 'Trees'],
            'algorithm': ['Sorting', 'Searching', 'Dynamic Programming'],
            'database': ['SQL', 'Queries', 'Normalization'],
            'machine': ['Models', 'Training', 'Evaluation']
        }
        
        for keyword in keywords:
            if keyword in topic_mapping:
                topics.extend(topic_mapping[keyword])
        
        return topics[:5] if topics else ['Core Concepts', 'Best Practices', 'Advanced Topics']
