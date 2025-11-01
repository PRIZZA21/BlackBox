# NOTE THIS IS A LEGACY CODE 
import assemblyai as aai
import ollama
import os
import soundfile as sf
import sounddevice as sd
import io
import sys
import time
import threading
from typing import Type
from gtts import gTTS
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

# Set API Keys
ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")

if not ASSEMBLYAI_API_KEY:
    raise ValueError("ASSEMBLYAI_API_KEY not set.")

EXIT_PHRASE = "Power off."

class AIVoiceAgent:
    def __init__(self):
        self.transcript = [{"role": "system", "content":
            "You are a professional and empathetic call center agent for a customer service department.\n"
            "Your role is to listen to customer complaints, understand their issues, and provide helpful solutions.\n"
            "Be patient, respectful, and acknowledge the customer's frustration.\n"
            "Ask clarifying questions to better understand the problem.\n"
            "Provide clear and concise solutions or next steps.\n"
            "Always maintain a professional and friendly tone.\n"
            "Show empathy and validate the customer's concerns.\n"
            "If you cannot resolve the issue, offer to escalate it to a supervisor.\n"
            "Keep your responses under 300 characters where possible.\n"
            "Use natural language, no emojis or special formatting.\n"
            "Start by greeting the customer warmly and asking how you can help today."
        }]
        self._keep_listening = True
        self.client = None
        self.user_input_received = False
        self.last_user_input = None
        self.transcription_thread = None

    def on_begin(self, client: Type[StreamingClient], event: BeginEvent):
        print("🎙️ Transcription session started.")

    def on_turn(self, client: Type[StreamingClient], event: TurnEvent):
        if event.transcript and event.end_of_turn:
            user_text = event.transcript.strip()
            if user_text.lower() == EXIT_PHRASE.lower():
                print("\n 🚪 Call ended by customer.")
                self._keep_listening = False
                if self.client:
                    try:
                        self.client.disconnect(terminate=True)
                    except:
                        pass
                return
            
            self.last_user_input = user_text
            self.user_input_received = True
            print(f"👤 Customer: {user_text}")
            
            # Disconnect to stop listening
            if self.client:
                try:
                    self.client.disconnect(terminate=True)
                except:
                    pass

    def on_terminated(self, client: Type[StreamingClient], event: TerminationEvent):
        pass

    def on_error(self, client: Type[StreamingClient], error: StreamingError):
        if "keepalive ping failed" not in str(error).lower():
            print(f"Transcription Error: {error}")

    def _transcription_thread_func(self):
        """Run transcription in a separate thread"""
        print("🎙️ Listening to customer...")
        self.user_input_received = False
        self.last_user_input = None
        
        self.client = StreamingClient(
            StreamingClientOptions(
                api_key=ASSEMBLYAI_API_KEY,
                api_host="streaming.assemblyai.com",
            )
        )
        
        self.client.on(StreamingEvents.Begin, self.on_begin)
        self.client.on(StreamingEvents.Turn, self.on_turn)
        self.client.on(StreamingEvents.Termination, self.on_terminated)
        self.client.on(StreamingEvents.Error, self.on_error)

        self.client.connect(
            StreamingParameters(
                sample_rate=16000,
                format_turns=True,
            )
        )
        
        try:
            self.client.stream(aai.extras.MicrophoneStream(sample_rate=16000))
        except Exception as e:
            if "keepalive ping failed" not in str(e).lower():
                print(f"Mic error: {e}")
        finally:
            if self.client:
                try:
                    self.client.disconnect(terminate=True)
                except:
                    pass

    def _start_transcription(self):
        """Start transcription in a background thread"""
        self.transcription_thread = threading.Thread(target=self._transcription_thread_func, daemon=True)
        self.transcription_thread.start()

    def _generate_response(self, user_message):
        """Generate AI response to customer message"""
        self.transcript.append({"role": "user", "content": user_message})
        
        try:
            ollama_stream = ollama.chat(
                model="gemma3:1b",
                messages=self.transcript,
                stream=True,
            )
        except Exception as e:
            print(f"Ollama Error: {e}")
            return

        print("☎️ Agent:", end=" ", flush=True)
        buffer = ""
        full_response = ""
        
        for chunk in ollama_stream:
            content = chunk['message']['content']
            buffer += content
            print(content, end="", flush=True)
            buffer = buffer.replace("**", "")
            
            if any(p in buffer for p in ['.', '?', '!', '\n']) or len(buffer) > 300:
                sentence = ""
                processed = False
                for p in reversed(['.', '?', '!', '\n']):
                    if p in buffer:
                        parts = buffer.split(p, 1)
                        sentence = parts[0] + p
                        buffer = parts[1] if len(parts) > 1 else ""
                        processed = True
                        break
                
                if not processed and len(buffer) > 300:
                    sentence = buffer
                    buffer = ""
                
                current_sentence = sentence.strip()
                if current_sentence:
                    full_response += current_sentence + " "
                    self._play_speech(current_sentence)
        
        remaining = buffer.strip()
        if remaining:
            print(remaining, end="", flush=True)
            full_response += remaining + " "
            self._play_speech(remaining)
        
        final_response = full_response.strip()
        if final_response:
            self.transcript.append({"role": "assistant", "content": final_response})
        
        print("\n" + "------------------------------------")

    def _play_speech(self, text: str):
        """Convert text to speech using gTTS"""
        if not text.strip():
            return
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            data, sr = sf.read(fp)
            sd.play(data, sr)
            sd.wait()
        except Exception as e:
            pass

    def _generate_initial_greeting(self):
        """Generate initial greeting from call center agent"""
        print("☎️ Agent:", end=" ", flush=True)
        initial_messages = self.transcript.copy()
        
        try:
            ollama_stream = ollama.chat(
                model="gemma3:1b",
                messages=initial_messages,
                stream=True,
            )
        except Exception as e:
            print(f"Ollama Error: {e}")
            return
        
        buffer = ""
        full_response = ""
        
        for chunk in ollama_stream:
            content = chunk['message']['content']
            buffer += content
            print(content, end="", flush=True)
            buffer = buffer.replace("**", "")
            
            if any(p in buffer for p in ['.', '?', '!', '\n']) or len(buffer) > 300:
                sentence = ""
                processed = False
                for p in reversed(['.', '?', '!', '\n']):
                    if p in buffer:
                        parts = buffer.split(p, 1)
                        sentence = parts[0] + p
                        buffer = parts[1] if len(parts) > 1 else ""
                        processed = True
                        break
                
                if not processed and len(buffer) > 300:
                    sentence = buffer
                    buffer = ""
                
                current_sentence = sentence.strip()
                if current_sentence:
                    full_response += current_sentence + " "
                    self._play_speech(current_sentence)
        
        remaining = buffer.strip()
        if remaining:
            print(remaining, end="", flush=True)
            full_response += remaining + " "
            self._play_speech(remaining)
        
        final_response = full_response.strip()
        if final_response:
            self.transcript.append({"role": "assistant", "content": final_response})
        
        print("\n" + "------------------------------------")

    def start(self):
        print(f"☎️ Call Center Agent Started... Say '{EXIT_PHRASE}' to end the call.\n")
        
        # Generate initial greeting
        self._generate_initial_greeting()
        
        # Main conversation loop
        while self._keep_listening:
            # Start transcription in background thread (non-blocking)
            self._start_transcription()
            
            # Wait for customer input with timeout
            wait_time = 0
            while not self.user_input_received and self._keep_listening and wait_time < 60:
                time.sleep(0.05)
                wait_time += 0.05
            
            # Generate response immediately
            if self.user_input_received and self.last_user_input:
                self._generate_response(self.last_user_input)
                self.user_input_received = False
                self.last_user_input = None
            elif wait_time >= 60:
                print("\n⏱️ Call timeout. Ending call.")
                self._keep_listening = False
        
        print("\n👋 Call Center Agent shut down. Thank you for calling!")

if __name__ == "__main__":
    try:
        AIVoiceAgent().start()
    except ValueError as e:
        print(f"Config Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


## REAL ESTATE DATASET

