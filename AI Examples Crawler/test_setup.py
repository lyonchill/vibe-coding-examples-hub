"""
Quick test script to verify your API keys are working
"""

import os
import sys

import requests
from dotenv import load_dotenv

try:
    import google.generativeai as genai
    from google.generativeai import types as genai_types
except ImportError:  # pragma: no cover
    genai = None
    genai_types = None

# Load environment variables
load_dotenv()

def test_youtube_api():
    """Test YouTube API key"""
    print("🔍 Testing YouTube API...")
    
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key or api_key == 'YOUR_KEY_HERE':
        print("❌ YouTube API key not set in .env file")
        return False
    
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': 'test',
            'type': 'video',
            'maxResults': 1,
            'key': api_key
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print("✅ YouTube API key is valid!")
            data = response.json()
            quota_remaining = response.headers.get('X-RateLimit-Remaining', 'Unknown')
            print(f"   Daily quota remaining: {quota_remaining}")
            return True
        else:
            print(f"❌ YouTube API error: {response.status_code}")
            print(f"   Response: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ YouTube API test failed: {e}")
        return False

def test_gemini_api():
    """Test Gemini API key"""
    print("\n🤖 Testing Gemini API...")

    if genai is None or genai_types is None:
        print("❌ google-generativeai 套件未安裝")
        return False

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_KEY_HERE":
        print("❌ Gemini API key not set in .env file")
        return False

    try:
        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        model = genai.GenerativeModel(model_name=model_name)

        response = model.generate_content(["說：API 測試成功"], request_options={"timeout": 15})

        parts = []
        for candidate in response.candidates or []:
            if candidate.finish_reason and candidate.finish_reason == 3:
                print("❌ Gemini response was blocked by safety settings")
                return False
            for part in getattr(candidate.content, "parts", []) or []:
                if getattr(part, "text", None):
                    parts.append(part.text)

        reply = " ".join(parts).strip()

        if reply:
            print("✅ Gemini API key is valid!")
            print(f"   Gemini response: {reply}")
            return True

        finish_reasons = [getattr(c, "finish_reason", None) for c in (response.candidates or [])]
        print(f"❌ Gemini API returned empty response (finish_reason={finish_reasons})")
        return False

    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def test_email_config():
    """Check email configuration"""
    print("\n📧 Checking email configuration...")
    
    email = os.getenv('EMAIL_TO')
    if not email or email == 'your-email@example.com':
        print("⚠️  Email not set in .env file")
        print("   (This won't prevent crawling, but you won't receive emails)")
        return False
    
    print(f"✅ Email set to: {email}")
    return True

def main():
    print("=" * 60)
    print("AI Examples Hub - Configuration Test")
    print("=" * 60)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\n❌ .env file not found!")
        print("   Please create a .env file and fill in your API keys, e.g.:")
        print("   YOUTUBE_API_KEY=your_youtube_key")
        print("   GEMINI_API_KEY=your_gemini_key")
        sys.exit(1)
    
    # Run tests
    youtube_ok = test_youtube_api()
    gemini_ok = test_gemini_api()
    email_ok = test_email_config()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if youtube_ok and gemini_ok:
        print("✅ All required APIs are working!")
        print("   You're ready to run: python ai_examples_crawler.py")
    else:
        print("❌ Some APIs are not configured correctly")
        print("   Please check the errors above and update your .env file")
    
    if not email_ok:
        print("⚠️  Email notification is not configured (optional)")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
