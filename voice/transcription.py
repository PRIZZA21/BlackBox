import threading
from typing import Type, Callable
import assemblyai as aai
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    TerminationEvent,
    TurnEvent,
)
from utils.logger import logger


class TranscriptionManager:
    """Manages audio transcription using AssemblyAI"""
    
    def __init__(self, api_key: str, sample_rate: int = 16000):
        """
        Initialize transcription manager
        
        Args:
            api_key: AssemblyAI API key
            sample_rate: Audio sample rate in Hz
        """
        self.api_key = api_key
        self.sample_rate = sample_rate
        self.client = None
        self.thread = None
        self.is_listening = False
        
        # Callbacks
        self.on_text_callback: Callable[[str], None] = None
        self.on_error_callback: Callable[[str], None] = None
    
    def set_on_text(self, callback: Callable[[str], None]):
        """Set callback for when text is transcribed"""
        self.on_text_callback = callback
    
    def set_on_error(self, callback: Callable[[str], None]):
        """Set callback for errors"""
        self.on_error_callback = callback
    
    def _on_begin(self, client: Type[StreamingClient], event: BeginEvent):
        """Callback when session begins"""
        logger.debug("Transcription session started")
        self.is_listening = True
    
    def _on_turn(self, client: Type[StreamingClient], event: TurnEvent):
        """Callback when speech turn is detected"""
        if event.transcript and event.end_of_turn:
            if self.on_text_callback:
                self.on_text_callback(event.transcript.strip())
            
            # Disconnect to stop listening
            if self.client:
                try:
                    self.client.disconnect(terminate=True)
                except Exception as e:
                    logger.error(f"Error disconnecting: {e}")
    
    def _on_terminated(self, client: Type[StreamingClient], event: TerminationEvent):
        """Callback when session terminates"""
        self.is_listening = False
        logger.debug("Transcription session closed")
    
    def _on_error(self, client: Type[StreamingClient], error: StreamingError):
        """Callback on error"""
        if "keepalive ping failed" not in str(error).lower():
            logger.error(f"Transcription error: {error}")
            if self.on_error_callback:
                self.on_error_callback(str(error))
    
    def _transcription_thread_func(self):
        """Run transcription in a separate thread"""
        try:
            self.client = StreamingClient(
                StreamingClientOptions(
                    api_key=self.api_key,
                    api_host="streaming.assemblyai.com",
                )
            )
            
            self.client.on(StreamingEvents.Begin, self._on_begin)
            self.client.on(StreamingEvents.Turn, self._on_turn)
            self.client.on(StreamingEvents.Termination, self._on_terminated)
            self.client.on(StreamingEvents.Error, self._on_error)

            self.client.connect(
                StreamingParameters(
                    sample_rate=self.sample_rate,
                    format_turns=True,
                )
            )
            
            self.client.stream(aai.extras.MicrophoneStream(sample_rate=self.sample_rate))
        except Exception as e:
            logger.error(f"Transcription thread error: {e}")
            if self.on_error_callback:
                self.on_error_callback(str(e))
        finally:
            if self.client:
                try:
                    self.client.disconnect(terminate=True)
                except:
                    pass
    
    def start(self):
        """Start listening for audio"""
        logger.info("Starting transcription...")
        self.thread = threading.Thread(
            target=self._transcription_thread_func,
            daemon=True
        )
        self.thread.start()
    
    def stop(self):
        """Stop listening"""
        if self.client:
            try:
                self.client.disconnect(terminate=True)
            except:
                pass
