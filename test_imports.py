#!/usr/bin/env python3
import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print("\nTesting imports...")

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ dotenv loaded")
except Exception as e:
    print(f"❌ dotenv error: {e}")
    sys.exit(1)

try:
    from config import config
    print(f"✅ config loaded")
except Exception as e:
    print(f"❌ config error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nAll imports successful!")
