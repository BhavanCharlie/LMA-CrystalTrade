#!/usr/bin/env python3
"""
Quick test script to verify OpenAI API key is working
"""
import os
import sys

# Load environment variables
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

api_key = os.getenv('OPENAI_API_KEY', '')

if not api_key:
    print("❌ OPENAI_API_KEY not found in .env file")
    sys.exit(1)

print(f"✅ Found OPENAI_API_KEY (length: {len(api_key)})")
print("Testing OpenAI connection...")

try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    # Simple test call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'Hello' if you can read this."}],
        max_tokens=10
    )
    
    print(f"✅ OpenAI API is working!")
    print(f"   Response: {response.choices[0].message.content}")
    print(f"\n🎉 Your API key is valid and ready to use!")
    print(f"\n📝 To use it:")
    print(f"   1. Restart your backend server")
    print(f"   2. Upload a new document")
    print(f"   3. The AI will extract real data from PDFs")
    
except Exception as e:
    print(f"❌ Error testing OpenAI API: {e}")
    print(f"\nPossible issues:")
    print(f"   - Invalid API key")
    print(f"   - Network connection problem")
    print(f"   - API quota exceeded")
    sys.exit(1)
