import soundfile as sf
import sounddevice as sd
import io
from gtts import gTTS
from utils.logger import logger


class SpeechSynthesizer:
    """Converts text to speech using gTTS"""
    
    def __init__(self, lang: str = 'en', slow: bool = False):
        """
        Initialize speech synthesizer
        
        Args:
            lang: Language code (default: 'en' for English)
            slow: Whether to speak slowly
        """
        self.lang = lang
        self.slow = slow
    
    def speak(self, text: str) -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to convert to speech
            
        Returns:
            True if successful, False otherwise
        """
        if not text.strip():
            return False
        
        try:
            logger.debug(f"Synthesizing speech for: {text[:50]}...")
            tts = gTTS(text=text, lang=self.lang, slow=self.slow)
            
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            data, sr = sf.read(fp)
            sd.play(data, sr)
            sd.wait()
            
            return True
        except Exception as e:
            logger.error(f"Speech synthesis error: {e}")
            return False
