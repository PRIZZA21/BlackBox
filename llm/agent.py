import time
from typing import List, Dict
import ollama
from utils.logger import logger


class RealEstateAgent:
    """Real estate agent powered by LLM with RAG"""
    
    SYSTEM_PROMPT = """You are a professional real estate agent assistant.
You help customers find properties and answer questions about real estate listings.
When a customer asks about properties, you will be provided with relevant property information from the database.
Always base your answers on the provided property data.
Be friendly, professional, and helpful.
If information about a specific detail is not provided, say so honestly.
Keep responses concise, under 300 characters when possible.
If multiple properties match, briefly mention the top options.
Greet customers warmly and ask how you can help them find their perfect property."""
    
    def __init__(self, model_name: str = "gemma3:1b"):
        """
        Initialize the agent
        
        Args:
            model_name: Name of the Ollama model to use
        """
        self.model_name = model_name
        self.conversation_history: List[Dict[str, str]] = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]
        logger.info(f"Initialized RealEstateAgent with model: {model_name}")
    
    def generate_greeting(self):
        """Generate initial greeting"""
        return self._generate_response("")
    
    def generate_response(self, user_message: str, context: str = "") -> str:
        """
        Generate AI response based on user input and context
        
        Args:
            user_message: User's spoken input
            context: Additional context (e.g., search results)
            
        Returns:
            Generated response text
        """
        # Create enhanced message with context
        if context:
            enhanced_message = f"Customer question: {user_message}\n\nRelevant property information:\n{context}\n\nPlease answer based on this information."
        else:
            enhanced_message = user_message
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": enhanced_message
        })
        
        return self._generate_response(enhanced_message)
    
    def _generate_response(self, user_message: str = "") -> str:
        """
        Internal method to generate response from LLM
        
        Args:
            user_message: User message (can be empty for initial greeting)
            
        Returns:
            Generated response
        """
        try:
            logger.debug(f"Generating response for: {user_message[:50]}...")
            
            ollama_stream = ollama.chat(
                model=self.model_name,
                messages=self.conversation_history,
                stream=True,
            )
            
            full_response = ""
            for chunk in ollama_stream:
                full_response += chunk['message']['content']
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response.strip()
            })
            
            return full_response.strip()
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error. Please try again."
    
    def split_response_by_sentences(self, response: str, max_chars: int = 300) -> List[str]:
        """
        Split response into sentences for incremental playback
        
        Args:
            response: Full response text
            max_chars: Maximum characters per sentence
            
        Returns:
            List of sentences
        """
        sentences = []
        buffer = ""
        
        for char in response:
            buffer += char
            if char in '.?!\n' or len(buffer) > max_chars:
                if buffer.strip():
                    sentences.append(buffer.strip())
                buffer = ""
        
        if buffer.strip():
            sentences.append(buffer.strip())
        
        return sentences

