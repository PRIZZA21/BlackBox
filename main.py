import time
from config import config
from data import RealEstateKnowledgeBase
from voice import TranscriptionManager, SpeechSynthesizer
from llm import RealEstateAgent
from utils import logger


class RealEstateVoiceAssistant:
    """Main application class coordinating all components"""
    
    def __init__(self):
        """Initialize all components"""
        logger.info("Initializing Real Estate Voice Assistant...")
        
        # Initialize components
        self.kb = RealEstateKnowledgeBase(config.CSV_FILE, config.EMBEDDING_MODEL)
        self.transcriber = TranscriptionManager(config.ASSEMBLYAI_API_KEY, config.SAMPLE_RATE)
        self.speaker = SpeechSynthesizer()
        self.agent = RealEstateAgent(config.LLM_MODEL)
        
        # State management
        self.is_running = True
        self.user_input = None
        self.user_input_received = False
        
        # Set up callbacks
        self.transcriber.set_on_text(self._on_user_spoke)
        self.transcriber.set_on_error(self._on_transcription_error)
        
        logger.info("Initialization complete!")
    
    def _on_user_spoke(self, text: str):
        """Callback when user speaks"""
        self.user_input = text
        self.user_input_received = True
        print(f"👤 Customer: {text}")
    
    def _on_transcription_error(self, error: str):
        """Callback on transcription error"""
        logger.error(f"Transcription error: {error}")
    
    def _should_exit(self, user_input: str) -> bool:
        """Check if user wants to exit"""
        return user_input.lower() == config.EXIT_PHRASE.lower()
    
    def _process_user_input(self, user_input: str):
        """Process user input and generate response"""
        # Check for exit
        if self._should_exit(user_input):
            print("\n 🚪 Call ended by customer.")
            self.is_running = False
            return
        
        # Search knowledge base
        logger.info(f"Searching knowledge base for: {user_input}")
        context = self.kb.search(user_input, n_results=3)
        
        # Generate response
        logger.info("Generating response...")
        response = self.agent.generate_response(user_input, context)
        print(f"🏠 Agent: {response}")
        
        # Split and play response
        sentences = self.agent.split_response_by_sentences(response)
        for sentence in sentences:
            self.speaker.speak(sentence)
        
        print("------------------------------------")
    
    def _wait_for_input(self, timeout: int = config.MAX_WAIT_TIME) -> bool:
        """
        Wait for user input with timeout
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if input received, False on timeout
        """
        start_time = time.time()
        self.user_input_received = False
        
        while not self.user_input_received and self.is_running:
            time.sleep(config.CHECK_INTERVAL)
            if time.time() - start_time > timeout:
                logger.warning("Input timeout")
                return False
        
        return self.user_input_received
    
    def start(self):
        """Start the voice assistant"""
        print(f"🏠 Real Estate Voice Assistant Started...")
        print(f"Say '{config.EXIT_PHRASE}' to end the call.\n")
        
        # Generate initial greeting
        logger.info("Generating greeting...")
        greeting = self.agent.generate_greeting()
        print(f"🏠 Agent: {greeting}\n")
        sentences = self.agent.split_response_by_sentences(greeting)
        for sentence in sentences:
            self.speaker.speak(sentence)
        
        print("------------------------------------\n")
        
        # Main conversation loop
        while self.is_running:
            # Start listening
            logger.info("Waiting for customer input...")
            self.transcriber.start()
            
            # Wait for input
            if self._wait_for_input():
                if self.user_input:
                    self._process_user_input(self.user_input)
                    self.user_input = None
            else:
                print("\n⏱️ No response detected. Ending call.")
                self.is_running = False
        
        print("\n👋 Thank you for using our real estate service!")
    
    def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up resources...")
        self.transcriber.stop()


def main():
    """Main entry point"""
    try:
        assistant = RealEstateVoiceAssistant()
        assistant.start()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Error: {e}")
    finally:
        if 'assistant' in locals():
            assistant.cleanup()


if __name__ == "__main__":
    main()
