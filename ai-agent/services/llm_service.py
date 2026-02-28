"""
LLM Service
Handles AI model interactions (Groq or Ollama)
"""

from typing import List, Dict, Optional
from groq import Groq
from config import Config
import streamlit as st

class LLMService:
    """Service for interacting with Large Language Models"""
    
    def __init__(self):
        """Initialize LLM client based on configuration"""
        self.provider = Config.LLM_PROVIDER
        self.model = Config.LLM_MODEL
        self.temperature = Config.LLM_TEMPERATURE
        self.max_tokens = Config.LLM_MAX_TOKENS
        self.client = None
        self.init_error = None
        
        if self.provider == 'groq':
            if not Config.GROQ_API_KEY or Config.GROQ_API_KEY == 'your_groq_api_key_here':
                self.init_error = "GROQ_API_KEY is not configured. Please add your API key to the .env file."
                st.warning(f"⚠️ {self.init_error}")
                self.client = None
            else:
                try:
                    self.client = Groq(api_key=Config.GROQ_API_KEY)
                    # Test the connection
                    st.success("✅ Groq LLM initialized successfully!")
                except Exception as e:
                    self.init_error = f"Failed to initialize Groq client: {str(e)}"
                    st.error(f"❌ {self.init_error}")
                    self.client = None
        else:
            self.init_error = f"Unsupported LLM provider: {self.provider}"
            st.warning(self.init_error)
            self.client = None
    
    def generate_response(
        self,
        user_message: str,
        context: str = "",
        web_results: Optional[List[Dict]] = None,
        chat_history: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate a response using the LLM
        
        Args:
            user_message: The user's message/question
            context: Additional context (user data, course info, etc.)
            web_results: Results from web search
            chat_history: Previous conversation messages
            system_prompt: Custom system prompt
            
        Returns:
            Generated response string
        """
        
        try:
            # Check if client is initialized
            if not self.client:
                error_msg = self.init_error or "LLM service is not available. Please configure your GROQ_API_KEY in the .env file and restart the app."
                return f"⚠️ {error_msg}"
            
            # Build system prompt
            if not system_prompt:
                system_prompt = self._build_system_prompt(context, web_results)
            
            # Build messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add chat history (last 10 messages for context)
            if chat_history:
                for msg in chat_history[-10:]:
                    if msg.get('role') in ['user', 'assistant']:
                        messages.append({
                            "role": msg['role'],
                            "content": msg['content']
                        })
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Generate response
            if self.provider == 'groq':
                response = self._generate_groq_response(messages)
            else:
                response = "LLM provider not configured properly."
            
            return response
            
        except Exception as e:
            error_details = f"LLM generation error: {str(e)}"
            st.error(f"❌ {error_details}")
            print(f"ERROR: {error_details}")  # Log to console
            import traceback
            print(traceback.format_exc())  # Print full stack trace
            return f"I apologize, but I encountered an error: {str(e)}\n\nPlease check your API key and try again."
    
    def _generate_groq_response(self, messages: List[Dict]) -> str:
        """Generate response using Groq API"""
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=1,
                stream=False
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    def _build_system_prompt(
        self,
        context: str,
        web_results: Optional[List[Dict]] = None
    ) -> str:
        """Build the system prompt for the LLM"""
        
        prompt_parts = [
            "You are an AI Study Assistant for TechVidya, an educational platform.",
            "Your role is to help students learn effectively by:",
            "- Answering questions about their courses and study materials",
            "- Providing clear explanations of technical concepts",
            "- Suggesting study strategies and resources",
            "- Recommending relevant practice problems and assessments",
            "",
            "Guidelines:",
            "- Be encouraging and supportive",
            "- Provide accurate, well-structured information",
            "- Use examples when explaining concepts",
            "- Cite sources when using web search results",
            "- If you don't know something, be honest about it",
            ""
        ]
        
        # Add user context
        if context:
            prompt_parts.extend([
                "Student Context:",
                context,
                ""
            ])
        
        # Add web search results
        if web_results:
            prompt_parts.append("Current Web Search Results:")
            for i, result in enumerate(web_results, 1):
                prompt_parts.append(
                    f"{i}. {result.get('title', 'Source')}: {result.get('content', '')[:200]}..."
                )
            prompt_parts.append("")
            prompt_parts.append(
                "Use the above search results to provide accurate, up-to-date information. "
                "Cite sources when relevant."
            )
        
        return "\n".join(prompt_parts)
    
    def generate_assessment_recommendations(
        self,
        course_name: str,
        course_description: str,
        difficulty: str,
        count: int = 5
    ) -> List[Dict]:
        """
        Generate assessment recommendations using LLM
        
        Args:
            course_name: Name of the course
            course_description: Course description
            difficulty: Target difficulty level
            count: Number of recommendations to generate
            
        Returns:
            List of assessment recommendation dictionaries
        """
        
        prompt = f"""Generate {count} specific assessment recommendations for a course titled "{course_name}".

Course Description: {course_description}
Target Difficulty: {difficulty}

For each assessment, provide:
1. Title (specific and descriptive)
2. Type (Quiz, Coding Challenge, Project, or MCQ Test)
3. Duration (realistic time estimate)
4. Description (2-3 sentences about what it covers)
5. Key Topics (3-5 main topics covered)

Format your response as a JSON array of objects with keys: title, type, duration, description, topics.
Only return the JSON array, no additional text."""

        try:
            messages = [
                {"role": "system", "content": "You are an educational assessment designer. Provide recommendations in valid JSON format only."},
                {"role": "user", "content": prompt}
            ]
            
            response = self._generate_groq_response(messages)
            
            # Parse JSON response
            import json
            try:
                recommendations = json.loads(response)
                return recommendations
            except json.JSONDecodeError:
                # Fallback to structured parsing
                return self._parse_recommendations_fallback(response, count)
                
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            return []
    
    def _parse_recommendations_fallback(self, response: str, count: int) -> List[Dict]:
        """Fallback parser for non-JSON responses"""
        # Simple fallback - return empty if parsing fails
        return []
