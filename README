# 🏠 Real Estate Voice Assistant

A professional AI-powered voice agent for real estate customer service. This application listens to customer queries via microphone, searches your property database, and provides intelligent responses using natural language processing.

---

## 📋 Features

- **🎤 Real-time Speech Recognition** - Listens to customer voice using AssemblyAI's Universal-Streaming API
- **🔍 Semantic Search** - Finds relevant properties using vector embeddings and ChromaDB
- **🤖 AI-Powered Responses** - Generates intelligent responses using Ollama LLM
- **🔊 Text-to-Speech** - Speaks responses back to customers using Google Text-to-Speech
- **💾 CSV Data Integration** - Load your property data from CSV files
- **🧵 Threaded Architecture** - Non-blocking operations for smooth conversation flow
- **📊 RAG (Retrieval-Augmented Generation)** - Grounds responses in your actual property data
- **📝 Comprehensive Logging** - Tracks all operations for debugging and monitoring

---

## 🏗️ Project Structure

```
real_estate_voice_agent/
├── config/                          # Configuration management
│   ├── __init__.py
│   └── settings.py                  # Central settings file
│
├── data/                            # Knowledge base & data handling
│   ├── __init__.py
│   └── knowledge_base.py            # CSV loading & vector embeddings
│
├── voice/                           # Audio I/O operations
│   ├── __init__.py
│   ├── transcription.py             # Speech-to-text (AssemblyAI)
│   └── speech_synthesis.py          # Text-to-speech (gTTS)
│
├── llm/                             # Language model operations
│   ├── __init__.py
│   └── agent.py                     # AI agent logic
│
├── utils/                           # Shared utilities
│   ├── __init__.py
│   └── logger.py                    # Logging configuration
│
├── .env                             # Environment variables (API keys)
├── .gitignore                       # Git ignore rules
├── main.py                          # Application entry point
├── requirements.txt                 # Project dependencies
├── real_estate_data.csv             # Property data
├── app.log                          # Application logs (auto-generated)
└── README.md                        # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Microphone for audio input
- Speakers for audio output
- AssemblyAI API key
- Ollama installed and running locally

### Installation

#### 1. Clone or Create Project

```bash
mkdir real_estate_voice_agent
cd real_estate_voice_agent
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv aai

# Activate it
# On Mac/Linux:
source aai/bin/activate

# On Windows:
aai\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# Mac/Linux:
echo "ASSEMBLYAI_API_KEY=sk_your_actual_api_key_here" > .env

# Windows PowerShell:
"ASSEMBLYAI_API_KEY=sk_your_actual_api_key_here" | Out-File -Encoding UTF8 .env
```

**Get your API key:** https://www.assemblyai.com/dashboard/api-keys

#### 5. Prepare Your Data

Create `real_estate_data.csv` with your property data:

```csv
Name,Property Title,Price,Location,Total_Area,Price_per_SQFT,Description,Baths,Balcony
Property 1,Beautiful House,850000,New York,1800,472,Modern 3 bed home with garden,2,1
Property 2,Luxury Apartment,1200000,Los Angeles,2400,500,4 bed luxury with pool,3,2
Property 3,Cozy Home,650000,Chicago,1400,464,Newly renovated 2 bed,2,1
```

#### 6. Start Ollama

In a separate terminal:

```bash
# Start Ollama server
ollama serve

# In another terminal, pull the model:
ollama pull gemma3:1b
```

#### 7. Run the Application

```bash
python main.py
```

Expected output:
```
============================================================
🏠 REAL ESTATE VOICE ASSISTANT
============================================================

🏠 Real Estate Voice Assistant Started...
Say 'Power off.' to end the call.

🏠 Agent: Hello! Welcome to our real estate service. 
I'm here to help you find your perfect property...

============================================================
🎙️ Listening for your response...
```

---

## 💬 Usage

### Starting a Conversation

1. Run `python main.py`
2. Wait for the agent's greeting
3. Speak your query clearly into the microphone
4. The agent will search the property database and respond
5. Say "Power off." to end the conversation

### Example Queries

- "Show me properties under 50 lakhs"
- "Tell me about properties in New York"
- "What 3 bedroom properties are available?"
- "Which properties have balconies?"
- "Find me luxury apartments with pools"
- "Show properties in the 1000 to 1500 range"

### Sample Conversation

```
👤 Customer: Tell me about properties in New York
🏠 Agent: I found a beautiful property at 123 Main Street in New York 
for $850,000. It's a 3-bedroom, 2-bathroom home with 1,800 square 
feet, featuring a modern kitchen, hardwood floors, and a backyard.
```

---

## 📁 Component Details

### config/settings.py

Central configuration management:

```python
from config import config

print(config.ASSEMBLYAI_API_KEY)  # API key
print(config.LLM_MODEL)            # "gemma3:1b"
print(config.SAMPLE_RATE)          # 16000 Hz
print(config.EXIT_PHRASE)          # "Power off."
```

### data/knowledge_base.py

Handles property data and semantic search:

```python
from data import RealEstateKnowledgeBase

kb = RealEstateKnowledgeBase("real_estate_data.csv")
results = kb.search("properties in NYC", n_results=3)
```

Features:
- Reads CSV files with property data
- Creates vector embeddings for semantic search
- Uses ChromaDB for vector storage
- Returns top N matching properties

### voice/transcription.py

Manages speech-to-text conversion:

```python
from voice import TranscriptionManager

transcriber = TranscriptionManager(api_key, sample_rate=16000)
transcriber.set_on_text(callback_function)
transcriber.start()
```

Features:
- Real-time microphone listening
- AssemblyAI integration
- Callback-based architecture
- Automatic turn detection

### voice/speech_synthesis.py

Handles text-to-speech conversion:

```python
from voice import SpeechSynthesizer

speaker = SpeechSynthesizer()
speaker.speak("Hello! How can I help you?")
```

Features:
- Google Text-to-Speech integration
- Automatic audio playback
- Multiple language support

### llm/agent.py

AI agent logic and response generation:

```python
from llm import RealEstateAgent

agent = RealEstateAgent(model_name="gemma3:1b")
response = agent.generate_response(user_message, context)
```

Features:
- Ollama LLM integration
- Conversation history tracking
- Context-aware responses
- Response splitting for playback

### utils/logger.py

Logging configuration:

```python
from utils import logger

logger.info("Application started")
logger.error("An error occurred")
logger.debug("Debug information")
```

Logs to:
- Console (stdout)
- File (app.log)

---

## 🔧 Configuration

### Changing the LLM Model

Edit `config/settings.py`:

```python
LLM_MODEL = "mistral"  # or any other Ollama model
```

Then install the model:

```bash
ollama pull mistral
```

### Adjusting Audio Settings

```python
SAMPLE_RATE = 16000  # Hz (quality vs performance tradeoff)
EXIT_PHRASE = "goodbye"  # Change exit command
```

### Modifying System Prompt

Edit `llm/agent.py`:

```python
SYSTEM_PROMPT = """Your custom system prompt here..."""
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `assemblyai` | Speech-to-text API |
| `ollama` | Local LLM runtime |
| `pandas` | CSV data handling |
| `chromadb` | Vector database |
| `sentence-transformers` | Text embeddings |
| `gtts` | Text-to-speech |
| `sounddevice` | Audio capture |
| `soundfile` | Audio file handling |
| `python-dotenv` | Environment variables |

See `requirements.txt` for exact versions.

---

## 🐛 Troubleshooting

### Problem: "ASSEMBLYAI_API_KEY not set"

**Solution:**
```bash
# Verify .env file exists
cat .env

# Create if missing:
echo "ASSEMBLYAI_API_KEY=sk_your_key_here" > .env

# Restart the application
python main.py
```

### Problem: "No module named 'chromadb'"

**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: "No microphone detected"

**Solution:**
- Check system audio settings
- Ensure microphone is connected
- Test with: `python -m sounddevice`

### Problem: Ollama connection error

**Solution:**
```bash
# Start Ollama in a new terminal
ollama serve

# Pull the model in another terminal
ollama pull gemma3:1b
```

### Problem: CSV file not found

**Solution:**
```bash
# Create sample CSV
cat > real_estate_data.csv << 'EOF'
Name,Property Title,Price,Location,Total_Area,Price_per_SQFT,Description,Baths,Balcony
Property 1,House,500000,NYC,2000,250,Nice home,2,1
EOF
```

### Problem: Nothing printed to terminal

**Solution:**
```bash
# Run with debugging
python -u main.py

# Or create test file
python test_imports.py
```

---

## 📊 Data Format

Your CSV should have these columns:

| Column | Type | Example |
|--------|------|---------|
| Name | String | Property 1 |
| Property Title | String | Beautiful House |
| Price | Number | 850000 |
| Location | String | New York |
| Total_Area | Number | 1800 |
| Price_per_SQFT | Number | 472 |
| Description | String | Modern home with garden |
| Baths | Number | 2 |
| Balcony | Number | 1 |

---

## 🔐 Security

### Protecting Your API Key

**DO:**
- Store API key in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables for secrets
- Never commit `.env` to Git

**DON'T:**
- Hardcode API keys in source files
- Share `.env` file publicly
- Commit `.env` to version control
- Log sensitive information

### .gitignore Example

```
.env
.env.local
*.log
__pycache__/
.DS_Store
.chromadb/
venv/
aai/
```

---

## 🚀 Performance Optimization

### Reduce Latency

```python
# In config/settings.py
CHECK_INTERVAL = 0.02  # Check more frequently (default: 0.05)
MAX_WAIT_TIME = 45     # Shorter timeout (default: 60)
```

### Handle Large Datasets

```python
# In data/knowledge_base.py
search_results = kb.search(query, n_results=5)  # Increase from 3
```

### Use Faster Model

```python
# In config/settings.py
LLM_MODEL = "neural-chat"  # Faster than gemma3:1b
```

---

## 🔄 Workflow Diagram

```
┌──────────────────────────────────────────────┐
│          User Speaks to Microphone           │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│   Transcription: Speech → Text (AssemblyAI) │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│     Search: Find Matching Properties (RAG)   │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│    LLM: Generate Response (Ollama)           │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│   Speech Synthesis: Text → Audio (gTTS)     │
└──────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│        User Hears Response via Speaker      │
└──────────────────────────────────────────────┘
```

---

## 📈 Extending the Project

### Add Database Support

Replace CSV with database in `data/knowledge_base.py`:

```python
def _load_database_data(self):
    """Load from database instead of CSV"""
    # Your database code here
```

### Add REST API

Create `api.py`:

```python
from fastapi import FastAPI
from main import RealEstateVoiceAssistant

app = FastAPI()

@app.post("/query")
def query(text: str):
    # Process query and return response
    pass
```

### Add Multiple Languages

```python
from voice import SpeechSynthesizer

speaker = SpeechSynthesizer(lang='es')  # Spanish
speaker.speak("Hola! ¿Cómo puedo ayudarte?")
```

### Add Conversation History Export

```python
import json

def export_conversation(agent, filename="conversation.json"):
    with open(filename, 'w') as f:
        json.dump(agent.conversation_history, f, indent=2)
```

---

## 📚 Documentation

- [AssemblyAI Docs](https://www.assemblyai.com/docs)
- [Ollama Documentation](https://ollama.ai/library)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)

---

## 🤝 Contributing

To contribute to this project:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🆘 Support

If you encounter issues:

1. Check the **Troubleshooting** section
2. Review the logs in `app.log`
3. Run `python test_imports.py` to diagnose
4. Check that all dependencies are installed

---

## 🎯 Next Steps

After setup:

1. ✅ Verify all components load without errors
2. ✅ Test with a sample query
3. ✅ Customize the system prompt in `llm/agent.py`
4. ✅ Add your property data to `real_estate_data.csv`
5. ✅ Deploy to production (optional)

---

## 📞 API Keys Required

| Service | Purpose | Get Key |
|---------|---------|---------|
| AssemblyAI | Speech-to-text | https://www.assemblyai.com/dashboard/api-keys |

---

## 💡 Pro Tips

- Use `ollama list` to see available models
- Monitor `app.log` for debugging
- Test individual components with `test_imports.py`
- Use vector search for better property matching
- Implement caching for frequently searched properties

---

## 🎓 Learning Resources

- [Building Voice Agents](https://www.assemblyai.com/blog)
- [RAG Explained](https://docs.llamaindex.ai/)
- [Local LLMs Guide](https://ollama.ai/)

---

**Created:** November 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅

Happy building! 🚀
