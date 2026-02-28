"""
Helper Utilities
General utility functions for the application
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

def format_duration(minutes: int) -> str:
    """
    Format duration in minutes to human-readable string
    
    Args:
        minutes: Duration in minutes
        
    Returns:
        Formatted duration string
    """
    if minutes < 60:
        return f"{minutes} mins"
    else:
        hours = minutes // 60
        mins = minutes % 60
        if mins == 0:
            return f"{hours} hrs"
        return f"{hours} hrs {mins} mins"

def calculate_difficulty_score(difficulty: str) -> int:
    """
    Convert difficulty level to numeric score
    
    Args:
        difficulty: Difficulty level string
        
    Returns:
        Numeric score (1-4)
    """
    difficulty_map = {
        'Beginner': 1,
        'Intermediate': 2,
        'Advanced': 3,
        'Expert': 4
    }
    return difficulty_map.get(difficulty, 2)

def parse_course_topics(course_name: str, course_description: str) -> List[str]:
    """
    Extract topics from course name and description
    
    Args:
        course_name: Name of the course
        course_description: Course description
        
    Returns:
        List of extracted topics
    """
    # Simple keyword extraction
    text = f"{course_name} {course_description}".lower()
    
    # Common technical keywords
    keywords = [
        'python', 'javascript', 'java', 'react', 'node', 'angular', 'vue',
        'database', 'sql', 'mongodb', 'api', 'rest', 'graphql',
        'html', 'css', 'frontend', 'backend', 'fullstack',
        'machine learning', 'ai', 'data science', 'algorithms',
        'cloud', 'aws', 'azure', 'docker', 'kubernetes',
        'testing', 'security', 'devops', 'git', 'agile'
    ]
    
    found_topics = []
    for keyword in keywords:
        if keyword in text:
            found_topics.append(keyword.title())
    
    return found_topics[:10]  # Limit to 10 topics

def truncate_text(text: str, max_length: int = 150) -> str:
    """
    Truncate text to specified length with ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'

def format_timestamp(dt: datetime = None) -> str:
    """
    Format datetime to readable string
    
    Args:
        dt: Datetime object (defaults to now)
        
    Returns:
        Formatted timestamp string
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%B %d, %Y %I:%M %p")

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def calculate_completion_percentage(completed: int, total: int) -> float:
    """
    Calculate completion percentage
    
    Args:
        completed: Number of completed items
        total: Total number of items
        
    Returns:
        Completion percentage
    """
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 2)

def group_by_category(items: List[Dict], category_key: str = 'category') -> Dict[str, List[Dict]]:
    """
    Group items by category
    
    Args:
        items: List of item dictionaries
        category_key: Key to use for categorization
        
    Returns:
        Dictionary with categories as keys and lists of items as values
    """
    grouped = {}
    for item in items:
        category = item.get(category_key, 'Uncategorized')
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(item)
    return grouped

def merge_dicts_safe(dict1: Dict, dict2: Dict) -> Dict:
    """
    Safely merge two dictionaries
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    result.update(dict2)
    return result

def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format
    
    Args:
        user_id: User ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    # MongoDB ObjectId is 24 characters hex string
    if not user_id or len(user_id) != 24:
        return False
    
    try:
        int(user_id, 16)  # Try to parse as hexadecimal
        return True
    except ValueError:
        return False

def format_list_with_oxford_comma(items: List[str]) -> str:
    """
    Format a list of items with Oxford comma
    
    Args:
        items: List of items
        
    Returns:
        Formatted string
    """
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """
    Safely load JSON with fallback
    
    Args:
        json_str: JSON string
        default: Default value if parsing fails
        
    Returns:
        Parsed JSON or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default
