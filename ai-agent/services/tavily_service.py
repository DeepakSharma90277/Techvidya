"""
Tavily Service
Handles web search and information retrieval using Tavily API
"""

from typing import List, Dict, Optional
from tavily import TavilyClient
from config import Config
import streamlit as st

class TavilyService:
    """Service for interacting with Tavily API for web search"""
    
    def __init__(self):
        """Initialize Tavily client"""
        self.client = None
        self.search_depth = Config.TAVILY_SEARCH_DEPTH
        self.max_results = Config.TAVILY_MAX_RESULTS
        
        if not Config.TAVILY_API_KEY or Config.TAVILY_API_KEY == 'your_tavily_api_key_here':
            st.warning("⚠️ TAVILY_API_KEY is not configured. Web search will be disabled. Please add your API key to the .env file.")
            self.client = None
        else:
            try:
                self.client = TavilyClient(api_key=Config.TAVILY_API_KEY)
            except Exception as e:
                st.error(f"Failed to initialize Tavily client: {str(e)}")
                self.client = None
    
    def search(
        self,
        query: str,
        max_results: Optional[int] = None,
        search_depth: Optional[str] = None,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Perform web search using Tavily
        
        Args:
            query: Search query
            max_results: Maximum number of results (default from config)
            search_depth: 'basic' or 'advanced' (default from config)
            include_domains: List of domains to include
            exclude_domains: List of domains to exclude
            
        Returns:
            List of search results with title, url, and content
        """
        
        try:
            # Check if client is initialized
            if not self.client:
                st.info("🔍 Web search is not available. Configure TAVILY_API_KEY in .env file to enable this feature.")
                return []
            
            # Use provided values or defaults
            max_results = max_results or self.max_results
            search_depth = search_depth or self.search_depth
            
            # Perform search
            response = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results,
                include_domains=include_domains,
                exclude_domains=exclude_domains,
                include_answer=True,
                include_raw_content=False
            )
            
            # Extract and format results
            results = []
            
            # Add the AI-generated answer if available
            if response.get('answer'):
                results.append({
                    'title': 'AI Summary',
                    'url': '#',
                    'content': response['answer'],
                    'score': 1.0
                })
            
            # Add search results
            for result in response.get('results', []):
                results.append({
                    'title': result.get('title', 'No title'),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'score': result.get('score', 0.0)
                })
            
            return results
            
        except Exception as e:
            st.error(f"Tavily search error: {str(e)}")
            return []
    
    def search_educational_content(
        self,
        topic: str,
        content_type: str = "tutorial"
    ) -> List[Dict]:
        """
        Search for educational content on a specific topic
        
        Args:
            topic: The topic to search for
            content_type: Type of content (tutorial, guide, course, etc.)
            
        Returns:
            List of educational resources
        """
        
        # Prioritize educational domains
        educational_domains = [
            'github.com',
            'stackoverflow.com',
            'medium.com',
            'dev.to',
            'freecodecamp.org',
            'w3schools.com',
            'mdn.mozilla.org',
            'geeksforgeeks.org',
            'tutorialspoint.com',
            'coursera.org',
            'udemy.com',
            'youtube.com'
        ]
        
        query = f"{topic} {content_type} complete guide"
        
        return self.search(
            query=query,
            max_results=5,
            include_domains=educational_domains
        )
    
    def search_assessment_resources(
        self,
        course_name: str,
        difficulty: str = "intermediate"
    ) -> List[Dict]:
        """
        Search for assessment and practice resources
        
        Args:
            course_name: Name of the course or subject
            difficulty: Difficulty level
            
        Returns:
            List of assessment resources
        """
        
        query = f"{course_name} {difficulty} practice tests quiz challenges"
        
        # Focus on platforms with assessments
        assessment_platforms = [
            'leetcode.com',
            'hackerrank.com',
            'codewars.com',
            'exercism.io',
            'w3schools.com',
            'freecodecamp.org',
            'testdome.com',
            'pluralsight.com'
        ]
        
        return self.search(
            query=query,
            max_results=5,
            include_domains=assessment_platforms
        )
    
    def get_context(self, query: str) -> str:
        """
        Get contextual information for a query
        
        Args:
            query: The query to get context for
            
        Returns:
            Formatted context string
        """
        
        results = self.search(query=query, max_results=3)
        
        if not results:
            return "No additional context found."
        
        context_parts = []
        
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"Source {i}: {result.get('title', 'Unknown')}\n"
                f"{result.get('content', '')[:300]}...\n"
            )
        
        return "\n".join(context_parts)
