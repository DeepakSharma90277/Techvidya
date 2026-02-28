"""
API Client
Handles communication with the TechVidya backend API
"""

import requests
from typing import Dict, Optional, List
from config import Config

class APIClient:
    """Client for TechVidya backend API"""
    
    def __init__(self):
        """Initialize API client"""
        self.base_url = Config.BACKEND_BASE_URL
        self.timeout = 10  # seconds
    
    def get_user_context(self, user_id: str) -> Optional[Dict]:
        """
        Get user context including profile and enrolled courses
        
        Args:
            user_id: User ID
            
        Returns:
            User context dictionary or None
        """
        
        try:
            # Try to fetch from backend
            response = requests.get(
                f"{self.base_url}/aiagent/user-context/{user_id}",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json().get('data')
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            # Backend might not be available, return None
            print(f"API Error: {e}")
            return None
    
    def get_user_enrolled_courses(self, user_id: str, token: str) -> List[Dict]:
        """
        Get user's enrolled courses
        
        Args:
            user_id: User ID
            token: Authentication token
            
        Returns:
            List of course dictionaries
        """
        
        try:
            response = requests.get(
                f"{self.base_url}/profile/getEnrolledCourses",
                headers={'Authorization': f'Bearer {token}'},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json().get('data', [])
            else:
                return []
                
        except requests.exceptions.RequestException:
            return []
    
    def save_assessment_recommendation(
        self,
        user_id: str,
        assessment_data: Dict
    ) -> bool:
        """
        Save assessment recommendation for user
        
        Args:
            user_id: User ID
            assessment_data: Assessment data to save
            
        Returns:
            True if successful, False otherwise
        """
        
        try:
            response = requests.post(
                f"{self.base_url}/aiagent/save-recommendation",
                json={
                    'userId': user_id,
                    'assessment': assessment_data
                },
                timeout=self.timeout
            )
            
            return response.status_code == 200
            
        except requests.exceptions.RequestException:
            return False
    
    def get_course_details(self, course_id: str) -> Optional[Dict]:
        """
        Get detailed information about a course
        
        Args:
            course_id: Course ID
            
        Returns:
            Course details dictionary or None
        """
        
        try:
            response = requests.post(
                f"{self.base_url}/course/getCourseDetails",
                json={'courseId': course_id},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json().get('data')
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None
    
    def test_connection(self) -> bool:
        """
        Test connection to backend API
        
        Returns:
            True if backend is reachable, False otherwise
        """
        
        try:
            response = requests.get(
                self.base_url.replace('/api/v1', ''),
                timeout=5
            )
            return response.status_code == 200
            
        except requests.exceptions.RequestException:
            return False

# Convenience function
def get_user_context(user_id: str) -> Optional[Dict]:
    """
    Convenience function to get user context
    
    Args:
        user_id: User ID
        
    Returns:
        User context dictionary or None
    """
    client = APIClient()
    return client.get_user_context(user_id)
