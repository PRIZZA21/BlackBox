#!/usr/bin/env python3
import sys
import os
import traceback


os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

print("\n" + "="*60)
print("🏠 REAL ESTATE VOICE ASSISTANT - DEBUG MODE")
print("="*60)

print(f"\nPython: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Virtual env: {sys.prefix}")

# Step 1: Check environment
print("\n" + "-"*60)
print("Step 1: Checking Environment...")
print("-"*60)

if os.path.exists(".env"):
    print("✅ .env file exists")
    with open(".env", "r") as f:
        for line in f:
            if "ASSEMBLYAI_API_KEY" in line:
                key_part = line.split("=")[1][:15]
                print(f"   API Key starts with: {key_part}...")
else:
    print("❌ .env file NOT found!")
    sys.exit(1)

if os.path.exists("real_estate_data.csv"):
    print("✅ real_estate_data.csv exists")
else:
    print("❌ real_estate_data.csv NOT found!")
    sys.exit(1)

# Step 2: Load config
print("\n" + "-"*60)
print("Step 2: Loading Configuration...")
print("-"*60)

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ dotenv loaded")
    
    from config import config
    print("✅ config module loaded")
    print(f"   CSV File: {config.CSV_FILE}")
    print(f"   API Key set: {bool(config.ASSEMBLYAI_API_KEY)}")
    
except Exception as e:
    print(f"❌ Config loading failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 3: Initialize components
print("\n" + "-"*60)
print("Step 3: Initializing Components...")
print("-"*60)

try:
    print("\n[3.1] Loading knowledge base...")
    from data import RealEstateKnowledgeBase
    kb = RealEstateKnowledgeBase(config.CSV_FILE, config.EMBEDDING_MODEL)
    print("✅ Knowledge base loaded")
    
except Exception as e:
    print(f"❌ Knowledge base failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n[3.2] Loading transcription manager...")
    from voice import TranscriptionManager
    transcriber = TranscriptionManager(config.ASSEMBLYAI_API_KEY, config.SAMPLE_RATE)
    print("✅ Transcription manager ready")
    
except Exception as e:
    print(f"❌ Transcription failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n[3.3] Loading speech synthesizer...")
    from voice import SpeechSynthesizer
    speaker = SpeechSynthesizer()
    print("✅ Speech synthesizer ready")
    
except Exception as e:
    print(f"❌ Speech synthesis failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n[3.4] Loading LLM agent...")
    from llm import RealEstateAgent
    agent = RealEstateAgent(config.LLM_MODEL)
    print("✅ LLM agent initialized")
    
except Exception as e:
    print(f"❌ LLM agent failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Step 4: Start assistant
print("\n" + "="*60)
print("✅ ALL COMPONENTS LOADED SUCCESSFULLY!")
print("="*60)

print("\n🏠 Real Estate Voice Assistant Started...")
print(f"Say '{config.EXIT_PHRASE}' to end the call.\n")

try:
    print("Generating initial greeting...")
    greeting = agent.generate_greeting()
    print(f"\n🏠 Agent: {greeting}\n")
    print("="*60)
    print("Ready to start conversation!")
    print("="*60)
    
except Exception as e:
    print(f"❌ Error generating greeting: {e}")
    traceback.print_exc()
    sys.exit(1)

